"""
Model Cache Manager - Optimized NLP Model Loading and Caching
File: model_cache.py

This module provides efficient model loading, caching, and management
to significantly reduce video generation time by avoiding repeated
model loading.
"""

import os
import time
import pickle
import logging
from typing import Dict, Any, Optional
from functools import lru_cache
import threading

# NLP
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# OCR 
import easyocr

class ModelCacheManager:
    """Singleton class to manage model loading and caching"""
    
    _instance = None
    _lock = threading.Lock()
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not getattr(self, '_initialized', False):
            self.logger = logging.getLogger(__name__)
            self.cache_dir = 'model_cache'
            os.makedirs(self.cache_dir, exist_ok=True)
            self._initialized = True
    
    @lru_cache(maxsize=3)
    def get_summarization_pipeline(self, model_name: str = 'sshleifer/distilbart-cnn-12-6'):
        """Get cached summarization pipeline"""
        cache_key = f"summarizer_{model_name.replace('/', '_')}"
        
        if cache_key in self._models:
            self.logger.info(f"Using cached summarization model: {model_name}")
            return self._models[cache_key]
        
        start_time = time.time()
        self.logger.info(f"Loading summarization model: {model_name}")
        
        try:
            # Use device auto-detection for GPU if available
            device = 0 if torch.cuda.is_available() else -1
            
            pipeline_obj = pipeline(
                'summarization', 
                model=model_name,
                device=device,
                model_kwargs={"torch_dtype": torch.float16 if torch.cuda.is_available() else torch.float32}
            )
            
            self._models[cache_key] = pipeline_obj
            load_time = time.time() - start_time
            self.logger.info(f"Model loaded in {load_time:.2f} seconds")
            
            return pipeline_obj
            
        except Exception as e:
            self.logger.error(f"Failed to load model {model_name}: {e}")
            # Fallback to smaller model
            if model_name != 't5-small':
                self.logger.info("Falling back to t5-small model")
                return self.get_summarization_pipeline('t5-small')
            raise
    
    def get_ocr_reader(self, languages=['en'], gpu=None):
        """Get cached OCR reader"""
        if gpu is None:
            gpu = torch.cuda.is_available()
            
        # Convert list to tuple for hashing
        lang_tuple = tuple(languages) if isinstance(languages, list) else (languages,)
        cache_key = f"ocr_{'_'.join(lang_tuple)}_{gpu}"
        
        if cache_key in self._models:
            self.logger.info("Using cached OCR reader")
            return self._models[cache_key]
        
        start_time = time.time()
        self.logger.info(f"Loading OCR reader for languages: {languages}")
        
        try:
            reader = easyocr.Reader(languages, gpu=gpu)
            self._models[cache_key] = reader
            
            load_time = time.time() - start_time
            self.logger.info(f"OCR reader loaded in {load_time:.2f} seconds")
            
            return reader
            
        except Exception as e:
            self.logger.error(f"Failed to load OCR reader: {e}")
            # Fallback without GPU
            if gpu:
                self.logger.info("Falling back to CPU OCR")
                return self.get_ocr_reader(languages, gpu=False)
            raise
    
    def preload_models(self, config: Dict[str, Any]):
        """Preload all models based on configuration"""
        self.logger.info("Preloading models for faster inference...")
        
        # Preload NLP model
        nlp_config = config.get('nlp', {})
        model_name = nlp_config.get('model', 'sshleifer/distilbart-cnn-12-6')
        self.get_summarization_pipeline(model_name)
        
        # Preload OCR reader
        ocr_config = config.get('ocr', {})
        languages = ocr_config.get('languages', ['en'])
        gpu_enabled = ocr_config.get('gpu_enabled', False)
        self.get_ocr_reader(languages, gpu_enabled)
        
        self.logger.info("Model preloading completed!")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        info = {
            'loaded_models': list(self._models.keys()),
            'model_count': len(self._models),
            'gpu_available': torch.cuda.is_available(),
            'cache_dir': self.cache_dir
        }
        return info
    
    def clear_cache(self):
        """Clear all cached models"""
        self.logger.info("Clearing model cache...")
        self._models.clear()
        self.get_summarization_pipeline.cache_clear()
        # Note: get_ocr_reader no longer uses lru_cache


# Global instance
model_cache = ModelCacheManager()


def get_fast_summarizer(model_name: str = 'sshleifer/distilbart-cnn-12-6'):
    """Get a fast cached summarization pipeline"""
    return model_cache.get_summarization_pipeline(model_name)


def get_fast_ocr_reader(languages=['en'], gpu=None):
    """Get a fast cached OCR reader"""
    return model_cache.get_ocr_reader(languages, gpu)


def preload_all_models(config: Dict[str, Any]):
    """Preload all models for the application"""
    model_cache.preload_models(config)


# Performance-optimized model recommendations
FAST_MODELS = {
    'summarization': {
        'ultra_fast': 't5-small',
        'fast': 'sshleifer/distilbart-cnn-12-6', 
        'balanced': 'facebook/bart-large-cnn',
        'quality': 'google/pegasus-large'
    }
}


def get_recommended_model(performance_level: str = 'fast') -> str:
    """Get recommended model based on performance needs"""
    return FAST_MODELS['summarization'].get(performance_level, 'sshleifer/distilbart-cnn-12-6')
