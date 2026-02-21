import json
from source.models.rule import ADRules

class JSONSerializer:
    """Utility class to serialize ADRules to JSON format."""

    @staticmethod
    def serialize_rules(rules: ADRules) -> str:
        """
        Serializes an ADRules object to a formatted JSON string.
        
        Args:
            rules (ADRules): The extracted rules object.
            
        Returns:
            str: JSON representation of the rules.
        """
        if not rules:
            return "{}"
            
        try:
            # Pydantic v2 method to dump to JSON with indentation
            return rules.model_dump_json(indent=2)
        except AttributeError:
            # Fallback for older Pydantic versions
            return rules.json(indent=2)
