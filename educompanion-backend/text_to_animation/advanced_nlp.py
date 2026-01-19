"""
Advanced NLP module for text processing and summarization
Includes text cleaning, keyword extraction, language detection, and multiple summarization strategies
"""

import re
import nltk
import spacy
from textblob import TextBlob
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass
import numpy as np

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

@dataclass
class SummaryResult:
    """Structured summary result with metadata"""
    summary: str
    keywords: List[str]
    confidence: float
    original_length: int
    summary_length: int
    compression_ratio: float
    language: str

class TextCleaner:
    """Advanced text cleaning and preprocessing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def clean_ocr_text(self, text: str) -> str:
        """Clean text specifically for OCR artifacts"""
        # Remove common OCR artifacts
        text = re.sub(r'[^\w\s\.,!?;:\-\(\)\[\]{}\"\'\/]', '', text)
        
        # Fix common OCR mistakes
        replacements = {
            r'\b0\b': 'O',  # Zero to letter O
            r'\b1\b': 'I',  # One to letter I (context dependent)
            r'rn': 'm',     # Common OCR mistake
            r'\s+': ' ',    # Multiple spaces to single
            r'([.!?])\s*([a-z])': r'\1 \2',  # Fix punctuation spacing
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)
        
        return text.strip()
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for better processing"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common punctuation issues
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        # Remove repeated characters (common in handwriting)
        text = re.sub(r'(.)\1{3,}', r'\1\1', text)
        
        return text.strip()
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using NLTK"""
        try:
            sentences = nltk.sent_tokenize(text)
            return [s.strip() for s in sentences if len(s.strip()) > 5]
        except:
            # Fallback to simple splitting
            sentences = re.split(r'[.!?]+', text)
            return [s.strip() for s in sentences if len(s.strip()) > 5]

class KeywordExtractor:
    """Extract important keywords and phrases from text"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.nlp = None
        self._load_spacy_model()
    
    def _load_spacy_model(self):
        """Load spaCy model for NER and keyword extraction"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.logger.warning("spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
    
    def extract_keywords_tfidf(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords using TF-IDF approach"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
            
            # Split into sentences for TF-IDF
            sentences = nltk.sent_tokenize(text)
            if len(sentences) < 2:
                sentences = [text]
            
            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words=list(ENGLISH_STOP_WORDS),
                ngram_range=(1, 2),
                min_df=1
            )
            
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Get top keywords
            top_indices = mean_scores.argsort()[-max_keywords:][::-1]
            keywords = [feature_names[i] for i in top_indices if mean_scores[i] > 0]
            
            return keywords
        except ImportError:
            self.logger.warning("scikit-learn not available for TF-IDF extraction")
            return self.extract_keywords_simple(text, max_keywords)
    
    def extract_keywords_simple(self, text: str, max_keywords: int = 10) -> List[str]:
        """Simple keyword extraction using TextBlob"""
        blob = TextBlob(text)
        
        # Get noun phrases
        noun_phrases = [str(phrase).lower() for phrase in blob.noun_phrases]
        
        # Get important words (nouns, adjectives)
        words = [word.lower() for word, pos in blob.tags 
                if pos.startswith(('NN', 'JJ')) and len(word) > 3]
        
        # Combine and get frequency
        all_terms = noun_phrases + words
        term_freq = {}
        
        for term in all_terms:
            term_freq[term] = term_freq.get(term, 0) + 1
        
        # Sort by frequency and return top terms
        sorted_terms = sorted(term_freq.items(), key=lambda x: x[1], reverse=True)
        return [term for term, freq in sorted_terms[:max_keywords]]
    
    def extract_named_entities(self, text: str) -> List[str]:
        """Extract named entities using spaCy"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = [ent.text for ent in doc.ents 
                   if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'PRODUCT']]
        return list(set(entities))

class AdvancedSummarizer:
    """Advanced text summarization with multiple strategies"""
    
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.text_cleaner = TextCleaner()
        self.keyword_extractor = KeywordExtractor()
        
        self.summarizer = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the summarization model"""
        try:
            model_name = self.config.get('model', 'facebook/bart-large-cnn')
            self.logger.info(f"Loading summarization model: {model_name}")
            
            self.summarizer = pipeline('summarization', model=model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            self.logger.info("Summarization model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load summarization model: {e}")
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the text"""
        try:
            blob = TextBlob(text)
            return blob.detect_language()
        except:
            return 'en'  # Default to English
    
    def preprocess_text(self, text: str) -> str:
        """Comprehensive text preprocessing"""
        # Clean OCR artifacts
        text = self.text_cleaner.clean_ocr_text(text)
        
        # Normalize text
        text = self.text_cleaner.normalize_text(text)
        
        return text
    
    def chunk_text(self, text: str, chunk_size: Optional[int] = None) -> List[str]:
        """Split text into chunks for processing"""
        if chunk_size is None:
            chunk_size = self.config.get('chunk_size', 1000)
        
        if not self.tokenizer:
            # Simple character-based chunking
            return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        # Token-based chunking
        tokens = self.tokenizer.encode(text)
        max_tokens = 1024  # Most models have this limit
        
        chunks = []
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i+max_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)
        
        return chunks
    
    def summarize_extractive(self, text: str, num_sentences: int = 3) -> str:
        """Extractive summarization using sentence ranking"""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            sentences = self.text_cleaner.split_into_sentences(text)
            if len(sentences) <= num_sentences:
                return text
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Calculate sentence similarities
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Score sentences based on similarity with other sentences
            sentence_scores = np.sum(similarity_matrix, axis=1)
            
            # Get top sentences
            top_indices = sentence_scores.argsort()[-num_sentences:][::-1]
            top_indices.sort()  # Maintain original order
            
            summary_sentences = [sentences[i] for i in top_indices]
            return ' '.join(summary_sentences)
            
        except ImportError:
            # Fallback: take first and last sentences plus random middle ones
            if len(sentences) <= num_sentences:
                return text
            
            selected = [sentences[0]]  # First sentence
            if num_sentences > 2:
                middle_count = num_sentences - 2
                middle_start = len(sentences) // 4
                middle_end = 3 * len(sentences) // 4
                middle_sentences = sentences[middle_start:middle_end]
                
                if len(middle_sentences) >= middle_count:
                    step = len(middle_sentences) // middle_count
                    selected.extend(middle_sentences[::step][:middle_count])
                else:
                    selected.extend(middle_sentences)
            
            if len(sentences) > 1:
                selected.append(sentences[-1])  # Last sentence
            
            return ' '.join(selected[:num_sentences])
    
    def summarize_abstractive(self, text: str) -> str:
        """Abstractive summarization using transformer model"""
        if not self.summarizer:
            return self.summarize_extractive(text)
        
        try:
            max_length = self.config.get('max_summary_length', 130)
            min_length = self.config.get('min_summary_length', 30)
            
            # Check if text is too short
            if len(text.split()) < min_length:
                return text
            
            # Chunk text if it's too long
            chunks = self.chunk_text(text)
            
            if len(chunks) == 1:
                # Single chunk
                result = self.summarizer(
                    text, 
                    max_length=max_length, 
                    min_length=min_length, 
                    do_sample=False
                )
                return result[0]['summary_text']
            else:
                # Multiple chunks - summarize each and combine
                chunk_summaries = []
                for chunk in chunks:
                    if len(chunk.strip()) > 50:  # Skip very short chunks
                        result = self.summarizer(
                            chunk, 
                            max_length=max_length//2, 
                            min_length=min_length//2, 
                            do_sample=False
                        )
                        chunk_summaries.append(result[0]['summary_text'])
                
                # Combine chunk summaries
                combined = ' '.join(chunk_summaries)
                
                # Final summarization if combined is still long
                if len(combined.split()) > max_length:
                    result = self.summarizer(
                        combined, 
                        max_length=max_length, 
                        min_length=min_length, 
                        do_sample=False
                    )
                    return result[0]['summary_text']
                else:
                    return combined
                    
        except Exception as e:
            self.logger.error(f"Abstractive summarization failed: {e}")
            return self.summarize_extractive(text)
    
    def summarize_text(self, text: str, strategy: str = "hybrid") -> SummaryResult:
        """Main summarization interface"""
        original_length = len(text.split())
        
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Detect language
        language = self.detect_language(processed_text)
        
        # Extract keywords
        if self.config.get('enable_keyword_extraction', True):
            keywords = self.keyword_extractor.extract_keywords_tfidf(processed_text)
        else:
            keywords = []
        
        # Generate summary based on strategy
        if strategy == "extractive":
            summary = self.summarize_extractive(processed_text)
        elif strategy == "abstractive":
            summary = self.summarize_abstractive(processed_text)
        else:  # hybrid
            # Try abstractive first, fall back to extractive
            summary = self.summarize_abstractive(processed_text)
            if len(summary.split()) < 10:  # If summary is too short, try extractive
                extractive_summary = self.summarize_extractive(processed_text)
                if len(extractive_summary.split()) > len(summary.split()):
                    summary = extractive_summary
        
        summary_length = len(summary.split())
        compression_ratio = summary_length / original_length if original_length > 0 else 0
        confidence = min(1.0, compression_ratio * 2)  # Simple confidence metric
        
        return SummaryResult(
            summary=summary,
            keywords=keywords,
            confidence=confidence,
            original_length=original_length,
            summary_length=summary_length,
            compression_ratio=compression_ratio,
            language=language
        )

def create_nlp_processor(config: dict) -> AdvancedSummarizer:
    """Factory function to create NLP processor with configuration"""
    return AdvancedSummarizer(config)
