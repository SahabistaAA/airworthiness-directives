from source.models.document import Document
from source.models.rule import ADRules
from source.ai.llm_parser import LLMParser
from source.ai.vlm_parser import VLMParser
from source.services.ocr import OCRService
from source.services.extractor import ExtractorService
from source.utils.logger import logger
from source.utils.pdf_detection import PDFDetector

class ParsingController:
    def __init__(self):
        self.parser = None

    def parse(self, document: Document) -> ADRules:
        """
        Parse document with some methods 

        Args:
            document (Document): Document to be parsed

        Returns:
            ADRules: Parsed rules
        """
        logger.info(f"Parsing document: {document.filename}")

        # 1. Use OCR / VLM for scanned pdf
        if PDFDetector.is_scanned_pdf(document.file_path):
            logger.info(f"Document {document.filename} is scanned, using OCR/VLM")
            try:
                # Try OCR first
                ocr_service = OCRService()
                document.text = ocr_service.ocr_pdf(document.file_path)

                if not document.text:
                    logger.warning(f"OCR failed for {document.filename}, trying VLM")
                    vlm_parser = VLMParser()
                    document.text = vlm_parser.parse(document.file_path)

                if not document.text:
                    logger.error(f"Both OCR and VLM failed for {document.filename}")
                    return ADRules(ad_id="ERROR", applicability_rules={})
            except Exception as e:
                logger.error(f"Error in OCR/VLM for {document.filename}: {e}")
                return ADRules(ad_id="ERROR", applicability_rules={})

        # 2. Use Text extracting
        extractor_service = ExtractorService()
        document.text = extractor_service.extract_text(document.file_path)

        if not document.text:
            logger.error(f"Text extraction failed for {document.filename}")
            return ADRules(ad_id="ERROR", applicability_rules={})

        # 3. Use LLM for parsing
        try:
            rules = self.parser.parse(document.text)
            logger.info(f"Successfully parsed rules for AD: {rules.ad_id}")
            return rules
        except Exception as e:
            logger.error(f"Error parsing document {document.filename}: {e}")
            return ADRules(ad_id="ERROR", applicability_rules={})
