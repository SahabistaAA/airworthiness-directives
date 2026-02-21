import pymupdf
from source.models.rule import ADRules

class ExtractorService:
    def __init__(self):
        self.file_path = None
        self.doc = None
        self.total_pages = 0

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from pdf using pymupdf

        Args:
            file_path (str): path to pdf file

        Returns:
            str: extracted text
        """
        self.file_path = file_path
        text = ""

        self.doc = pymupdf.open(self.file_path)

        for page in self.doc:
            text += page.get_text()

        return text
        
    def parse(self, ad_id: str, text: str) -> ADRules:
        """
        Dummy parse method to satisfy the ParsingController interface.
        ExtractorService purely extracts raw text, so this returns empty rules.
        """
        from source.models.rule import ADApplicabilityRules
        return ADRules(
            ad_id=ad_id,
            applicability_rules=ADApplicabilityRules(
                aircraft_models=[],
                msn_constraints=[],
                excluded_if_modifications=[],
                required_modifications=[]
            )
        )
        