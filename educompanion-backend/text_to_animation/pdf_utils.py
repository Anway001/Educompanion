"""
PDF Processing Utilities
Converts PDF files to images for OCR processing
"""

import os
import tempfile
from pathlib import Path
from typing import List, Optional
import logging

# PDF processing libraries
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMU_PDF_AVAILABLE = True
except ImportError:
    PYMU_PDF_AVAILABLE = False

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF to image conversion for OCR processing"""

    def __init__(self):
        self.temp_dir = None

    def convert_pdf_to_images(self, pdf_path: str, dpi: int = 300, fmt: str = 'PNG') -> List[str]:
        """
        Convert PDF pages to images

        Args:
            pdf_path: Path to PDF file
            dpi: DPI for image conversion (higher = better quality but slower)
            fmt: Image format (PNG, JPEG, etc.)

        Returns:
            List of image file paths
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create temporary directory for images
        self.temp_dir = tempfile.mkdtemp(prefix='pdf_images_')

        image_paths = []

        try:
            if PDF2IMAGE_AVAILABLE:
                image_paths = self._convert_with_pdf2image(pdf_path, dpi, fmt)
            elif PYMU_PDF_AVAILABLE:
                image_paths = self._convert_with_pymupdf(pdf_path, dpi, fmt)
            else:
                raise ImportError("No PDF processing library available. Install pdf2image or PyMuPDF")

        except Exception as e:
            logger.error(f"PDF conversion failed: {e}")
            raise

        logger.info(f"Converted PDF to {len(image_paths)} images")
        return image_paths

    def _convert_with_pdf2image(self, pdf_path: str, dpi: int, fmt: str) -> List[str]:
        """Convert PDF using pdf2image library"""
        try:
            # Convert PDF pages to PIL images
            pil_images = convert_from_path(pdf_path, dpi=dpi)

            image_paths = []
            for i, pil_image in enumerate(pil_images):
                # Save PIL image to file
                image_path = os.path.join(self.temp_dir, f'page_{i+1:03d}.{fmt.lower()}')
                pil_image.save(image_path, format=fmt.upper())
                image_paths.append(image_path)

            return image_paths

        except Exception as e:
            logger.error(f"pdf2image conversion failed: {e}")
            raise

    def _convert_with_pymupdf(self, pdf_path: str, dpi: int, fmt: str) -> List[str]:
        """Convert PDF using PyMuPDF library"""
        try:
            pdf_document = fitz.open(pdf_path)
            image_paths = []

            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)

                # Convert page to pixmap
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))

                # Save pixmap to file
                image_path = os.path.join(self.temp_dir, f'page_{page_num+1:03d}.{fmt.lower()}')
                pix.save(image_path)
                image_paths.append(image_path)

            pdf_document.close()
            return image_paths

        except Exception as e:
            logger.error(f"PyMuPDF conversion failed: {e}")
            raise

    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
                logger.info("Cleaned up temporary PDF images")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp directory: {e}")

def convert_pdf_to_images(pdf_path: str, output_dir: Optional[str] = None, dpi: int = 300) -> List[str]:
    """
    Convenience function to convert PDF to images

    Args:
        pdf_path: Path to PDF file
        output_dir: Output directory (creates temp dir if None)
        dpi: DPI for conversion

    Returns:
        List of image file paths
    """
    processor = PDFProcessor()

    try:
        if output_dir:
            # Use specified output directory
            os.makedirs(output_dir, exist_ok=True)
            processor.temp_dir = output_dir

        return processor.convert_pdf_to_images(pdf_path, dpi)
    except Exception as e:
        logger.error(f"PDF conversion failed: {e}")
        raise

def is_pdf_file(file_path: str) -> bool:
    """Check if file is a PDF"""
    return Path(file_path).suffix.lower() == '.pdf'

def get_pdf_page_count(pdf_path: str) -> int:
    """Get number of pages in PDF"""
    if not PYMU_PDF_AVAILABLE:
        logger.warning("PyMuPDF not available for page count")
        return 0

    try:
        pdf_document = fitz.open(pdf_path)
        page_count = pdf_document.page_count
        pdf_document.close()
        return page_count
    except Exception as e:
        logger.error(f"Failed to get page count: {e}")
        return 0
