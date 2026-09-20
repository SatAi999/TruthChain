import re
from typing import List, Dict, Any, Tuple

class NormalizationEngine:
    # Entity Alias maps
    ENTITY_MAPPINGS = {
        "COMPANY_A": [
            "company a", "company a ltd", "company a limited", "company a inc",
            "company a corp", "company a technologies", "supplier a", "vendor a"
        ],
        "HOSPITAL_X": [
            "hospital x", "hospital x medical center", "hospital x health",
            "hospital x clinic", "receiving site x"
        ],
        "MEDICAL_DEVICE_10K": [
            "medical devices", "devices", "medical device units", "units", "product catalog #md-10k"
        ]
    }

    @classmethod
    def resolve_entity(cls, text: str) -> Tuple[str, str, float]:
        """
        Resolves an entity text snippet into (canonical_id, display_name, confidence).
        """
        clean_text = text.lower().strip()
        
        for canonical_id, aliases in cls.ENTITY_MAPPINGS.items():
            for alias in aliases:
                if alias in clean_text or clean_text in alias:
                    display_name = canonical_id.replace("_", " ").title()
                    return canonical_id, display_name, 0.95

        # Fallback default canonicalization
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', text).strip().title()
        canonical_id = f"ENT_{re.sub(r'\\s+', '_', clean_name).upper()}"
        return canonical_id, clean_name, 0.70
