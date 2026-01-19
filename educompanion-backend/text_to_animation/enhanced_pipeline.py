"""
Enhanced Text-to-Animation Pipeline
Main integration file that combines all components into a cohesive system
"""

import os
import yaml
import logging
import argparse
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Import enhanced modules
from enhanced_ocr import create_ocr_engine
from advanced_nlp import create_nlp_processor, SummaryResult
from enhanced_animation import create_animation_engine

@dataclass
class PipelineResult:
    """Complete pipeline result with all intermediate outputs"""
    extracted_text: str
    summary_result: SummaryResult
    video_path: str
    audio_path: str
    processing_time: float
    intermediate_files: Dict[str, str]

class TextToAnimationPipeline:
    """Main pipeline orchestrator"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        
        # Initialize components
        self.ocr_engine = None
        self.nlp_processor = None
        self.animation_engine = None
        
        # Setup working directory
        self.temp_dir = self.config.get('output', {}).get('temp_directory', 'ttm_tmp')
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Configuration file {config_path} not found! Using defaults.")
            return self._get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing configuration: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'ocr': {
                'languages': ['en'],
                'gpu_enabled': False,
                'confidence_threshold': 0.7,
                'preprocessing': {
                    'gaussian_blur': True,
                    'denoise': True,
                    'contrast_enhancement': True,
                    'resize_factor': 2.0
                }
            },
            'nlp': {
                'model': 'facebook/bart-large-cnn',
                'max_summary_length': 130,
                'min_summary_length': 30,
                'chunk_size': 1000,
                'enable_keyword_extraction': True
            },
            'animation': {
                'resolution': {'width': 1280, 'height': 720},
                'fps': 24,
                'slide_duration': 4.0,
                'transition_duration': 0.5,
                'background_color': [255, 255, 255],
                'text_color': [0, 0, 0],
                'animation_style': 'fade'
            },
            'output': {
                'temp_directory': 'ttm_tmp',
                'video_codec': 'libx264',
                'audio_codec': 'aac',
                'keep_intermediate_files': False
            }
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_config.get('file', 'text_to_animation.log')),
                logging.StreamHandler() if log_config.get('enable_console', True) else logging.NullHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def initialize_components(self):
        """Initialize all pipeline components"""
        self.logger.info("Initializing pipeline components...")
        
        try:
            # Initialize OCR engine
            if self.ocr_engine is None:
                self.logger.info("Loading OCR engine...")
                self.ocr_engine = create_ocr_engine(self.config.get('ocr', {}))
            
            # Initialize NLP processor
            if self.nlp_processor is None:
                self.logger.info("Loading NLP processor...")
                self.nlp_processor = create_nlp_processor(self.config.get('nlp', {}))
            
            # Initialize animation engine
            if self.animation_engine is None:
                self.logger.info("Loading animation engine...")
                self.animation_engine = create_animation_engine(self.config.get('animation', {}))
            
            self.logger.info("All components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    def extract_text(self, image_path: str, method: str = "hybrid") -> str:
        """Extract text from image using OCR"""
        self.logger.info(f"Extracting text from {image_path} using {method} method")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        if self.ocr_engine is None:
            raise RuntimeError("OCR engine not initialized. Call initialize_components() first.")
        
        extracted_text = self.ocr_engine.extract_text_from_image(image_path, method)
        
        self.logger.info(f"Extracted {len(extracted_text)} characters")
        return extracted_text
    
    def process_text(self, text: str, strategy: str = "hybrid") -> SummaryResult:
        """Process and summarize text using NLP"""
        self.logger.info("Processing and summarizing text")
        
        if self.nlp_processor is None:
            raise RuntimeError("NLP processor not initialized. Call initialize_components() first.")
        
        summary_result = self.nlp_processor.summarize_text(text, strategy)
        
        self.logger.info(f"Generated summary with {summary_result.summary_length} words")
        return summary_result
    
    def generate_audio(self, text: str, output_path: str) -> str:
        """Generate audio from text using TTS"""
        self.logger.info("Generating audio from text")
        
        try:
            from gtts import gTTS
            
            tts_config = self.config.get('tts', {})
            language = tts_config.get('language', 'en')
            
            tts = gTTS(text=text, lang=language)
            tts.save(output_path)
            
            self.logger.info(f"Audio saved to {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"TTS generation failed: {e}")
            raise
    
    def create_animation(self, summary_result: SummaryResult, audio_path: str, output_path: str) -> str:
        """Create animated video from summary and audio"""
        self.logger.info("Creating animated video")
        
        if self.animation_engine is None:
            raise RuntimeError("Animation engine not initialized. Call initialize_components() first.")
        
        # Create slide configurations
        slide_configs = self.animation_engine.split_text_into_slides(
            summary_result.summary,
            summary_result.keywords
        )
        
        # Generate video
        video_path = self.animation_engine.create_video_from_slides(
            slide_configs,
            audio_path,
            output_path
        )
        
        self.logger.info(f"Video saved to {video_path}")
        return video_path
    
    def run_pipeline(self, input_image: str, output_video: str, 
                    ocr_method: str = "hybrid", 
                    nlp_strategy: str = "hybrid") -> PipelineResult:
        """Run the complete pipeline"""
        start_time = time.time()
        self.logger.info(f"Starting pipeline for {input_image}")
        
        try:
            # Initialize components
            self.initialize_components()
            
            # Step 1: OCR
            self.logger.info("Step 1: Text extraction")
            extracted_text = self.extract_text(input_image, ocr_method)
            
            if not extracted_text.strip():
                raise ValueError("No text could be extracted from the image")
            
            # Step 2: NLP Processing
            self.logger.info("Step 2: Text processing and summarization")
            summary_result = self.process_text(extracted_text, nlp_strategy)
            
            # Step 3: TTS
            self.logger.info("Step 3: Audio generation")
            audio_path = os.path.join(self.temp_dir, "tts_output.mp3")
            self.generate_audio(summary_result.summary, audio_path)
            
            # Step 4: Animation
            self.logger.info("Step 4: Video generation")
            video_path = self.create_animation(summary_result, audio_path, output_video)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Collect intermediate files
            intermediate_files = {
                'audio': audio_path,
                'temp_directory': self.temp_dir
            }
            
            # Cleanup if configured
            if not self.config.get('output', {}).get('keep_intermediate_files', False):
                self.cleanup_intermediate_files(intermediate_files)
            
            self.logger.info(f"Pipeline completed successfully in {processing_time:.2f} seconds")
            
            return PipelineResult(
                extracted_text=extracted_text,
                summary_result=summary_result,
                video_path=video_path,
                audio_path=audio_path,
                processing_time=processing_time,
                intermediate_files=intermediate_files
            )
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            raise
    
    def cleanup_intermediate_files(self, intermediate_files: Dict[str, str]):
        """Clean up intermediate files"""
        self.logger.info("Cleaning up intermediate files")
        
        try:
            for file_type, file_path in intermediate_files.items():
                if file_type != 'temp_directory' and os.path.exists(file_path):
                    os.remove(file_path)
                    self.logger.debug(f"Removed {file_path}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup some files: {e}")
    
    def batch_process(self, input_directory: str, output_directory: str) -> List[PipelineResult]:
        """Process multiple images in batch"""
        self.logger.info(f"Starting batch processing: {input_directory} -> {output_directory}")
        
        os.makedirs(output_directory, exist_ok=True)
        
        # Find all image files
        image_extensions = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        image_files = [
            f for f in os.listdir(input_directory)
            if Path(f).suffix.lower() in image_extensions
        ]
        
        results = []
        
        for i, image_file in enumerate(image_files):
            self.logger.info(f"Processing {i+1}/{len(image_files)}: {image_file}")
            
            input_path = os.path.join(input_directory, image_file)
            output_path = os.path.join(output_directory, f"{Path(image_file).stem}_animation.mp4")
            
            try:
                result = self.run_pipeline(input_path, output_path)
                results.append(result)
                self.logger.info(f"Successfully processed {image_file}")
            except Exception as e:
                self.logger.error(f"Failed to process {image_file}: {e}")
                continue
        
        self.logger.info(f"Batch processing completed. Processed {len(results)}/{len(image_files)} files")
        return results

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description="Text-to-Animation AI Pipeline")
    parser.add_argument('--input', required=True, help='Input image path')
    parser.add_argument('--output', default='output_animation.mp4', help='Output video path')
    parser.add_argument('--config', default='config.yaml', help='Configuration file path')
    parser.add_argument('--ocr-method', default='hybrid', 
                       choices=['hybrid', 'easyocr', 'tesseract'],
                       help='OCR method to use')
    parser.add_argument('--nlp-strategy', default='hybrid',
                       choices=['hybrid', 'abstractive', 'extractive'],
                       help='NLP summarization strategy')
    parser.add_argument('--batch', action='store_true',
                       help='Process all images in input directory')
    parser.add_argument('--streamlit', action='store_true',
                       help='Launch Streamlit web interface')
    
    args = parser.parse_args()
    
    if args.streamlit:
        # Launch Streamlit app
        import subprocess
        subprocess.run(['streamlit', 'run', 'enhanced_streamlit_app.py'])
        return
    
    # Initialize pipeline
    pipeline = TextToAnimationPipeline(args.config)
    
    try:
        if args.batch:
            # Batch processing
            if not os.path.isdir(args.input):
                print(f"Error: {args.input} is not a directory")
                return
            
            output_dir = args.output if os.path.isdir(args.output) else 'batch_output'
            results = pipeline.batch_process(args.input, output_dir)
            
            print(f"Batch processing completed. Processed {len(results)} files.")
            print(f"Output directory: {output_dir}")
        else:
            # Single file processing
            result = pipeline.run_pipeline(
                args.input, 
                args.output,
                args.ocr_method,
                args.nlp_strategy
            )
            
            print("Pipeline completed successfully!")
            print(f"Video saved to: {result.video_path}")
            print(f"Processing time: {result.processing_time:.2f} seconds")
            print(f"Summary: {result.summary_result.summary}")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
