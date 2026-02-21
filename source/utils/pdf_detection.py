import pymupdf
from source.utils.logger import logger

class PDFDetector:
    @staticmethod
    def is_scanned_pdf(file_path: str, text_threshold: int = 50) -> bool:
        """
        Detect whether a PDF is considered a "scanned" document (mostly images) 
        or a digital document containing real text.
        
        It does this by attempting to extract text from the first few pages. 
        If the total extracted text length is below a threshold, it's considered scanned.

        Args:
            file_path (str): The path to the PDF file.
            text_threshold (int): The minimum number of characters to consider it a text PDF.

        Returns:
            bool: True if it appears to be a scanned PDF (little to no text), False otherwise.
        """
        try:
            doc = pymupdf.open(file_path)
            
            # Check up to the first 3 pages to be efficient
            pages_to_check = min(3, len(doc))
            total_text_length = 0
            
            for i in range(pages_to_check):
                page = doc[i]
                text = page.get_text().strip()
                total_text_length += len(text)
                
                # If we've found enough text, it's not a scanned PDF
                if total_text_length >= text_threshold:
                    doc.close()
                    return False
                    
            doc.close()
            # If we checked the pages and didn't find enough text, it's scanned
            return total_text_length < text_threshold
            
        except Exception as e:
            # Fallback: assume it needs OCR if we can't open/parse it properly
            logger.error(f"Error analyzing PDF {file_path}: {e}")
            return True
