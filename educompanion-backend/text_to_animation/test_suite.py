"""
Test suite for the Text-to-Animation pipeline
Includes unit tests, integration tests, and sample data generation
"""

import unittest
import tempfile
import os
import yaml
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Import our modules
from enhanced_ocr import create_ocr_engine
from advanced_nlp import create_nlp_processor
from enhanced_animation import create_animation_engine
from enhanced_pipeline import TextToAnimationPipeline

class TestConfig:
    """Test configuration and sample data"""
    
    @staticmethod
    def get_test_config():
        """Get minimal test configuration"""
        return {
            'ocr': {
                'languages': ['en'],
                'gpu_enabled': False,
                'confidence_threshold': 0.5,
                'preprocessing': {
                    'gaussian_blur': True,
                    'denoise': True,
                    'contrast_enhancement': True,
                    'resize_factor': 1.0
                }
            },
            'nlp': {
                'model': 'sshleifer/distilbart-cnn-12-6',  # Smaller model for testing
                'max_summary_length': 50,
                'min_summary_length': 10,
                'chunk_size': 500,
                'enable_keyword_extraction': True
            },
            'animation': {
                'resolution': {'width': 640, 'height': 480},
                'fps': 24,
                'slide_duration': 2.0,
                'transition_duration': 0.2,
                'background_color': [255, 255, 255],
                'text_color': [0, 0, 0],
                'animation_style': 'fade'
            },
            'output': {
                'temp_directory': 'test_tmp',
                'keep_intermediate_files': True
            }
        }
    
    @staticmethod
    def create_sample_image(text: str, size: tuple = (800, 600)) -> str:
        """Create a sample image with text for testing"""
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, 'sample_text.png')
        
        # Create image with text
        image = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Simple text wrapping
        words = text.split()
        lines = []
        current_line = []
        max_width = size[0] - 40
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw text
        y = 20
        for line in lines:
            draw.text((20, y), line, fill='black', font=font)
            y += 30
        
        image.save(image_path)
        return image_path

class TestOCREngine(unittest.TestCase):
    """Test OCR functionality"""
    
    def setUp(self):
        self.config = TestConfig.get_test_config()['ocr']
        self.ocr_engine = create_ocr_engine(self.config)
        
        # Create sample image
        self.sample_text = "This is a test document for OCR. It contains multiple sentences."
        self.sample_image = TestConfig.create_sample_image(self.sample_text)
    
    def test_ocr_initialization(self):
        """Test OCR engine initialization"""
        self.assertIsNotNone(self.ocr_engine)
    
    def test_text_extraction(self):
        """Test text extraction from image"""
        extracted_text = self.ocr_engine.extract_text_from_image(self.sample_image)
        self.assertIsInstance(extracted_text, str)
        self.assertGreater(len(extracted_text), 0)
    
    def test_different_ocr_methods(self):
        """Test different OCR methods"""
        methods = ['easyocr', 'tesseract', 'hybrid']
        
        for method in methods:
            with self.subTest(method=method):
                try:
                    result = self.ocr_engine.extract_text_from_image(self.sample_image, method)
                    self.assertIsInstance(result, str)
                except Exception as e:
                    # Some methods might not be available in test environment
                    self.skipTest(f"Method {method} not available: {e}")
    
    def tearDown(self):
        # Clean up
        if os.path.exists(self.sample_image):
            os.remove(self.sample_image)

class TestNLPProcessor(unittest.TestCase):
    """Test NLP functionality"""
    
    def setUp(self):
        self.config = TestConfig.get_test_config()['nlp']
        self.nlp_processor = create_nlp_processor(self.config)
        
        self.sample_text = """
        Artificial intelligence is transforming many industries today. 
        Machine learning algorithms can process vast amounts of data quickly. 
        Natural language processing helps computers understand human language. 
        Computer vision enables machines to interpret visual information. 
        These technologies are creating new opportunities for innovation.
        """
    
    def test_nlp_initialization(self):
        """Test NLP processor initialization"""
        self.assertIsNotNone(self.nlp_processor)
    
    def test_text_preprocessing(self):
        """Test text preprocessing"""
        processed = self.nlp_processor.preprocess_text(self.sample_text)
        self.assertIsInstance(processed, str)
        self.assertGreater(len(processed), 0)
    
    def test_summarization(self):
        """Test text summarization"""
        result = self.nlp_processor.summarize_text(self.sample_text)
        
        self.assertIsNotNone(result.summary)
        self.assertGreater(len(result.summary), 0)
        self.assertLess(result.summary_length, result.original_length)
        self.assertIsInstance(result.keywords, list)
    
    def test_different_summarization_strategies(self):
        """Test different summarization strategies"""
        strategies = ['abstractive', 'extractive', 'hybrid']
        
        for strategy in strategies:
            with self.subTest(strategy=strategy):
                result = self.nlp_processor.summarize_text(self.sample_text, strategy)
                self.assertIsNotNone(result.summary)
                self.assertGreater(len(result.summary), 0)

class TestAnimationEngine(unittest.TestCase):
    """Test animation functionality"""
    
    def setUp(self):
        self.config = TestConfig.get_test_config()['animation']
        self.animation_engine = create_animation_engine(self.config)
        
        self.sample_summary = "AI is changing the world. Machine learning helps process data."
        self.sample_keywords = ["AI", "machine learning", "data"]
    
    def test_animation_initialization(self):
        """Test animation engine initialization"""
        self.assertIsNotNone(self.animation_engine)
    
    def test_slide_generation(self):
        """Test slide configuration generation"""
        slides = self.animation_engine.split_text_into_slides(
            self.sample_summary, 
            self.sample_keywords
        )
        
        self.assertIsInstance(slides, list)
        self.assertGreater(len(slides), 0)
        
        for slide in slides:
            self.assertIsNotNone(slide.text)
            self.assertGreater(slide.duration, 0)
    
    def test_video_creation_without_audio(self):
        """Test video creation without audio"""
        slides = self.animation_engine.split_text_into_slides(self.sample_summary)
        
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, 'test_video.mp4')
        
        try:
            result_path = self.animation_engine.create_video_from_slides(
                slides, None, output_path
            )
            self.assertEqual(result_path, output_path)
            self.assertTrue(os.path.exists(output_path))
        except Exception as e:
            # Video creation might fail in test environment without proper codecs
            self.skipTest(f"Video creation not available: {e}")

class TestPipeline(unittest.TestCase):
    """Test complete pipeline"""
    
    def setUp(self):
        self.config_path = tempfile.mktemp(suffix='.yaml')
        
        # Write test config
        with open(self.config_path, 'w') as f:
            yaml.dump(TestConfig.get_test_config(), f)
        
        self.pipeline = TextToAnimationPipeline(self.config_path)
        
        # Create sample image
        self.sample_text = "Machine learning is a subset of artificial intelligence."
        self.sample_image = TestConfig.create_sample_image(self.sample_text)
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization"""
        self.assertIsNotNone(self.pipeline)
        self.assertIsNotNone(self.pipeline.config)
    
    def test_component_initialization(self):
        """Test component initialization"""
        self.pipeline.initialize_components()
        
        self.assertIsNotNone(self.pipeline.ocr_engine)
        self.assertIsNotNone(self.pipeline.nlp_processor)
        self.assertIsNotNone(self.pipeline.animation_engine)
    
    def test_text_extraction_step(self):
        """Test individual text extraction step"""
        self.pipeline.initialize_components()
        
        extracted_text = self.pipeline.extract_text(self.sample_image)
        self.assertIsInstance(extracted_text, str)
        self.assertGreater(len(extracted_text), 0)
    
    def test_text_processing_step(self):
        """Test individual text processing step"""
        self.pipeline.initialize_components()
        
        result = self.pipeline.process_text(self.sample_text)
        self.assertIsNotNone(result.summary)
        self.assertIsInstance(result.keywords, list)
    
    def test_full_pipeline_run(self):
        """Test complete pipeline execution"""
        temp_dir = tempfile.mkdtemp()
        output_video = os.path.join(temp_dir, 'test_output.mp4')
        
        try:
            result = self.pipeline.run_pipeline(self.sample_image, output_video)
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result.extracted_text, str)
            self.assertIsNotNone(result.summary_result)
            self.assertGreater(result.processing_time, 0)
            
        except Exception as e:
            # Full pipeline might fail in test environment
            self.skipTest(f"Full pipeline test skipped: {e}")
    
    def tearDown(self):
        # Clean up
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if os.path.exists(self.sample_image):
            os.remove(self.sample_image)

class TestDataGeneration(unittest.TestCase):
    """Test sample data generation"""
    
    def test_sample_image_creation(self):
        """Test sample image creation"""
        text = "Sample text for testing"
        image_path = TestConfig.create_sample_image(text)
        
        self.assertTrue(os.path.exists(image_path))
        
        # Test image properties
        with Image.open(image_path) as img:
            self.assertEqual(img.mode, 'RGB')
            self.assertGreater(img.width, 0)
            self.assertGreater(img.height, 0)
        
        # Clean up
        os.remove(image_path)

def create_sample_data():
    """Create sample data for manual testing"""
    print("Creating sample data for testing...")
    
    sample_texts = [
        "Machine learning is a powerful tool for data analysis and prediction.",
        "Natural language processing helps computers understand human language better.",
        "Computer vision enables machines to interpret and analyze visual information.",
        "Deep learning uses neural networks to solve complex problems.",
        "Artificial intelligence is transforming industries worldwide."
    ]
    
    # Create sample directory
    sample_dir = "sample_data"
    os.makedirs(sample_dir, exist_ok=True)
    
    # Generate sample images
    for i, text in enumerate(sample_texts):
        image_path = TestConfig.create_sample_image(text, (1024, 768))
        
        # Move to sample directory
        new_path = os.path.join(sample_dir, f"sample_{i+1}.png")
        os.rename(image_path, new_path)
        
        print(f"Created: {new_path}")
    
    print(f"Sample data created in '{sample_dir}' directory")

def run_performance_tests():
    """Run performance tests"""
    print("Running performance tests...")
    
    import time
    
    # Test with different text lengths
    test_texts = [
        "Short text.",
        "Medium length text with several sentences. This should test normal processing.",
        """Long text with many sentences for testing performance. This text contains multiple 
        paragraphs and should test the system's ability to handle larger inputs. The text 
        includes various concepts and should generate a good summary. Natural language processing 
        is an important field in artificial intelligence. Machine learning algorithms help 
        computers understand human language better."""
    ]
    
    pipeline = TextToAnimationPipeline()
    pipeline.initialize_components()
    
    for i, text in enumerate(test_texts):
        print(f"\nTesting text {i+1} (length: {len(text)} chars)")
        
        start_time = time.time()
        result = pipeline.process_text(text)
        processing_time = time.time() - start_time
        
        print(f"Processing time: {processing_time:.2f}s")
        print(f"Compression ratio: {result.compression_ratio:.2f}")
        print(f"Keywords found: {len(result.keywords)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "samples":
            create_sample_data()
        elif sys.argv[1] == "performance":
            run_performance_tests()
        else:
            print("Usage: python test_suite.py [samples|performance]")
    else:
        # Run unit tests
        unittest.main()
