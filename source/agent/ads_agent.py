from source.ai.llm_parser import LLMParser
from source.ai.vlm_parser import VLMParser
from source.services.ocr import OCRService
from source.services.extractor import ExtractorService
from source.utils.logger import logger
from source.utils.pdf_detection import PDFDetector
from source.ai.hybrid_parser import HybridParser
from source.models.document import Document
from source.models.aircraft import AircraftConfiguration
from source.models.rule import ADRules

class ADSAgent:
    def __init__(self):
        self.llm_parser = LLMParser()
        self.vlm_parser = VLMParser()
        self.ocr_service = OCRService()
        self.extractor_service = ExtractorService()
        self.pdf_detector = PDFDetector()
        self._active_parser = None
    
    def _mode(self, mode: str = "default"):
        if mode == "default":
            self._active_parser = LLMParser()
        elif mode == "vlm":
            self._active_parser = VLMParser()
        elif mode == "ocr":
            self._active_parser = OCRService()
        elif mode == "extractor":
            self._active_parser = ExtractorService()
        elif mode == "hybrid":
            self._active_parser = HybridParser()
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def ingest(self, document: Document) -> ADRules:
        # TODO: Implement ingest
        pass

    def parser(self, document: Document) -> ADRules:
        # TODO: Implement parser
        pass

    def evaluator(self, rules: ADRules, aircraft: AircraftConfiguration) -> bool:
        # TODO: Implement evaluator
        pass

    def process_document(self, document: Document) -> ADRules:
        from source.controller.parsing import ParsingController
        pc = ParsingController()
        if self._active_parser:
            pc.parser = self._active_parser
        else:
            pc.parser = self.llm_parser # default
        
        logger.info(f"Using parser mode: {pc.parser.__class__.__name__}")
        return pc.parse(document)

    def run(self, document: Document, aircraft: AircraftConfiguration) -> bool:
        rules = self.process_document(document)
        from source.controller.evaluation import EvaluationController
        evaluator = EvaluationController()
        return evaluator.evaluate(rules, aircraft)