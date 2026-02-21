from source.models.rule import ADRules
from source.models.aircraft import AircraftConfiguration
from source.utils.logger import logger
import re

class EvaluationController:
    def evaluate(self, rules: ADRules, aircraft: AircraftConfiguration) -> str:
        """
        Determine if the aircraft is affected by the AD based on the extracted rules.

        Args:
            rules (ADRules): Parsed rules from the AD
            aircraft (AircraftConfiguration): Aircraft configuration

        Returns:
            str: 'Affected', 'Not Affected', or 'Not Applicable'
        """
        if not rules:
            return "ERROR"

        # 1. Check Aircraft Model
        # Simple string matching for now (e.g. "A320-214" matches "A320-214")
        model_match = False
        if rules.applicability_rules.aircraft_models:
            if aircraft.model in rules.applicability_rules.aircraft_models:
                model_match = True
        
        if not model_match:
            # TODO: Check for generic "Series" matches if required
            return "Not Applicable"
        
        # 2. Check MSN Constraints
        if rules.applicability_rules.msn_constraints:
            msn_match = False
            aircraft_msn = aircraft.msn
            # Try to convert to int for range comparisons
            try:
                msn_int = int(aircraft_msn)
            except ValueError:
                msn_int = None
                
            for constraint in rules.applicability_rules.msn_constraints:
                constraint = str(constraint).strip()
                # Exact match
                if constraint == aircraft_msn:
                    msn_match = True
                    break
                
                # Range match (e.g. "4500-5000" or "4500 to 5000")
                if "-" in constraint:
                    parts = constraint.split("-")
                    if len(parts) == 2:
                        try:
                            start = int(parts[0].strip())
                            end = int(parts[1].strip())
                            if msn_int is not None and start <= msn_int <= end:
                                msn_match = True
                                break
                        except ValueError:
                            pass
                elif " to " in constraint.lower():
                    parts = constraint.lower().split(" to ")
                    if len(parts) == 2:
                        try:
                            start = int(parts[0].strip())
                            end = int(parts[1].strip())
                            if msn_int is not None and start <= msn_int <= end:
                                msn_match = True
                                break
                        except ValueError:
                            pass
            
            if not msn_match:
                logger.info(f"Aircraft {aircraft.msn} excluded by MSN constraints.")
                return "Not Affected"

        def _is_mod_match(mod1: str, mod2: str) -> bool:
            def extract_id(s: str) -> str:
                # Extracts numbers with 4+ digits OR dashed alphanumeric sequences (like A320-57-1089)
                match = re.search(r'([A-Z0-9]+-[A-Z0-9-]+|\d{4,})', s.upper())
                return match.group(1) if match else s.lower()
            
            id1 = extract_id(mod1)
            id2 = extract_id(mod2)
            return id1 == id2 or id1 in mod2.upper() or id2 in mod1.upper()

        # 3. Check Excluded Modifications 
        if rules.applicability_rules.excluded_if_modifications:
            for ex_mod in rules.applicability_rules.excluded_if_modifications:
                if any(_is_mod_match(mod, ex_mod) for mod in aircraft.modifications):
                    logger.info(f"Aircraft {aircraft.msn} excluded by mod {ex_mod}")
                    return "Not Affected"
        
        # 4. Check Required Modifications
        if rules.applicability_rules.required_modifications:
            has_required = False
            for req_mod in rules.applicability_rules.required_modifications:
                if any(_is_mod_match(mod, req_mod) for mod in aircraft.modifications):
                    has_required = True
                    break
            
            if not has_required:
                logger.info(f"Aircraft {aircraft.msn} missing required mod for applicability.")
                return "Not Affected"
        
        return "Affected"