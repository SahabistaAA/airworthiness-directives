import re
from logger import logger

class Validators:
    @staticmethod
    def validate_ad_id(ad_id: str) -> bool:
        """
        Validates AD ID format (e.g. FAA-2025-23-53, 2025-0254).

        Args:
            ad_id (str): AD ID to validate

        Returns:
            bool: True if AD ID is valid, False otherwise
        """
        if not ad_id:
            return False
        
        # Basic regex for Year-Number pattern
        pattern = r'.*20\d{2}[-]\d{2,4}[-]?\d{0,4}.*'
        is_valid = bool(re.match(pattern, ad_id))

        if not is_valid:
            logger.warning(f"Invalid AD ID format: {ad_id}")
        return is_valid

    @staticmethod
    def validate_msn(msn: str) -> bool:
        """
        Validate MSN (Manufacturer Serial Number)

        Args:
            msn (str): MSN to validate

        Returns:
            bool: True if MSN is valid, False otherwise
        """
        if not msn:
            return False
        
        # Basic validation for MSN
        pattern = r'^[A-Za-z0-9-]+$'
        is_valid = bool(re.match(pattern, msn))

        if not is_valid:
            logger.warning(f"Invalid MSN format: {msn}")
        return is_valid