from typing import List, Optional
from pydantic import BaseModel

class ADApplicabilityRules(BaseModel):
    aircraft_models: List[str] = []
    msn_constraints: Optional[List[str]] = None # Could be ranges or list of MSNs
    excluded_if_modifications: List[str] = []
    required_modifications: List[str] = []

class ADRules(BaseModel):
    ad_id: str
    applicability_rules: ADApplicabilityRules