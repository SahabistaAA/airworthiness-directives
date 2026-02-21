import os
import io
import pymupdf
import pytesseract
from PIL import Image

from source.models.rule import ADRules

from source.utils.logger import logger

class OCRService:
    def __init__(self):
        pass

    def ocr_pdf(self, file_path: str, lang: str = "eng") -> str:
        """
        Extract text from pdf using pytesseract

        Args:
            file_path (str): path to pdf file

        Returns:
            str: extracted text
        """
        doc = pymupdf.open(file_path)

        full_text = []
        for i in range(len(doc)):
            logger.info(f"Processing page {i+1} of {len(doc)}")
            page = doc[i]
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img, lang=lang)
            full_text.append(text)

        return "\n\n--- Page Break ---\n\n".join(full_text)
    
    def parse(self, file_path: str) -> ADRules:
        # TODO: Implement OCR parsing
        pass