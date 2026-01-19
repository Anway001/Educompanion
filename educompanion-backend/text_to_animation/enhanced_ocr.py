"""
Enhanced OCR module for handwritten notes processing
Includes preprocessing, multiple OCR engines, and confidence scoring
"""

import cv2
import numpy as np
import easyocr
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass

@dataclass
class OCRResult:
    """Structured OCR result with confidence and bounding boxes"""
    text: str
    confidence: float
    bbox: Optional[Tuple[int, int, int, int]] = None
    engine: str = "unknown"

class ImagePreprocessor:
    """Advanced image preprocessing for better OCR results"""
    
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """Apply comprehensive image enhancement"""
        # Convert to PIL for some operations
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Resize if specified
        if self.config.get('resize_factor', 1.0) != 1.0:
            factor = self.config['resize_factor']
            new_size = (int(pil_image.width * factor), int(pil_image.height * factor))
            pil_image = pil_image.resize(new_size, Image.LANCZOS)
        
        # Enhance contrast
        if self.config.get('contrast_enhancement', True):
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.5)
        
        # Convert back to OpenCV format
        enhanced = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Denoise
        if self.config.get('denoise', True):
            enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        # Gaussian blur for smoothing
        if self.config.get('gaussian_blur', True):
            enhanced = cv2.GaussianBlur(enhanced, (1, 1), 0)
        
        return enhanced
    
    def binarize_image(self, image: np.ndarray) -> np.ndarray:
        """Convert to binary image for better text recognition"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return binary
    
    def deskew_image(self, image: np.ndarray) -> np.ndarray:
        """Correct image skew using Hough line detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        if lines is not None:
            angles = []
            for rho, theta in lines[:10]:  # Use first 10 lines
                angle = theta * 180 / np.pi - 90
                angles.append(angle)
            
            if angles:
                median_angle = np.median(angles)
                if abs(median_angle) > 0.5:  # Only correct if skew is significant
                    (h, w) = image.shape[:2]
                    center = (w // 2, h // 2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                    image = cv2.warpAffine(image, rotation_matrix, (w, h), 
                                         flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return image

class EnhancedOCR:
    """Enhanced OCR with multiple engines and preprocessing"""
    
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.preprocessor = ImagePreprocessor(config.get('preprocessing', {}))
        
        # Initialize OCR engines
        self.easyocr_reader = None
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        
        self._init_easyocr()
    
    def _init_easyocr(self):
        """Initialize EasyOCR reader"""
        try:
            languages = self.config.get('languages', ['en'])
            gpu_enabled = self.config.get('gpu_enabled', False)
            self.easyocr_reader = easyocr.Reader(languages, gpu=gpu_enabled)
            self.logger.info(f"EasyOCR initialized with languages: {languages}")
        except Exception as e:
            self.logger.error(f"Failed to initialize EasyOCR: {e}")
    
    def extract_text_easyocr(self, image_path: str) -> List[OCRResult]:
        """Extract text using EasyOCR with confidence scores"""
        if not self.easyocr_reader:
            return []
        
        try:
            results = self.easyocr_reader.readtext(image_path, detail=1)
            ocr_results = []
            
            for bbox, text, confidence in results:
                if confidence >= self.confidence_threshold:
                    # Convert bbox to (x, y, w, h) format
                    x_coords = [point[0] for point in bbox]
                    y_coords = [point[1] for point in bbox]
                    x, y = int(min(x_coords)), int(min(y_coords))
                    w, h = int(max(x_coords) - x), int(max(y_coords) - y)
                    
                    ocr_results.append(OCRResult(
                        text=text.strip(),
                        confidence=confidence,
                        bbox=(x, y, w, h),
                        engine="easyocr"
                    ))
            
            return ocr_results
        except Exception as e:
            self.logger.error(f"EasyOCR extraction failed: {e}")
            return []
    
    def extract_text_tesseract(self, image_path: str) -> List[OCRResult]:
        """Extract text using Tesseract OCR"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return []
            
            # Preprocess image
            processed = self.preprocessor.enhance_image(image)
            processed = self.preprocessor.deskew_image(processed)
            binary = self.preprocessor.binarize_image(processed)
            
            # Extract text with data
            data = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)
            
            ocr_results = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                text = data['text'][i].strip()
                confidence = float(data['conf'][i]) / 100.0  # Convert to 0-1 range
                
                if text and confidence >= self.confidence_threshold:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    
                    ocr_results.append(OCRResult(
                        text=text,
                        confidence=confidence,
                        bbox=(x, y, w, h),
                        engine="tesseract"
                    ))
            
            return ocr_results
        except Exception as e:
            self.logger.error(f"Tesseract extraction failed: {e}")
            return []
    
    def extract_text_hybrid(self, image_path: str) -> str:
        """Combine results from multiple OCR engines for better accuracy"""
        # Get results from both engines
        easyocr_results = self.extract_text_easyocr(image_path)
        tesseract_results = self.extract_text_tesseract(image_path)
        
        # Combine and deduplicate results
        all_results = easyocr_results + tesseract_results
        
        if not all_results:
            return ""
        
        # Sort by confidence and combine text
        all_results.sort(key=lambda x: x.confidence, reverse=True)
        
        # Simple deduplication and combination
        seen_texts = set()
        final_text_parts = []
        
        for result in all_results:
            if result.text.lower() not in seen_texts and len(result.text) > 2:
                seen_texts.add(result.text.lower())
                final_text_parts.append(result.text)
        
        return " ".join(final_text_parts)
    
    def extract_text_from_image(self, image_path: str, method: str = "hybrid") -> str:
        """Main interface for text extraction"""
        self.logger.info(f"Extracting text from {image_path} using {method} method")
        
        if method == "easyocr":
            results = self.extract_text_easyocr(image_path)
            return " ".join([r.text for r in results])
        elif method == "tesseract":
            results = self.extract_text_tesseract(image_path)
            return " ".join([r.text for r in results])
        else:  # hybrid
            return self.extract_text_hybrid(image_path)
    
    def get_text_regions(self, image_path: str) -> List[OCRResult]:
        """Get detailed text regions with bounding boxes"""
        easyocr_results = self.extract_text_easyocr(image_path)
        tesseract_results = self.extract_text_tesseract(image_path)
        
        # Combine and return all regions
        return easyocr_results + tesseract_results

def create_ocr_engine(config: dict) -> EnhancedOCR:
    """Factory function to create OCR engine with configuration"""
    return EnhancedOCR(config)
