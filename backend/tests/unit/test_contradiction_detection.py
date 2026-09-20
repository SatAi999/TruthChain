import pytest
from app.services.contradiction_engine import ContradictionEngine

def test_contradiction_detection():
    facts = [
        {"value": "Invoice INV-8821 for 10,000 units", "source_name": "INV-8821.txt"},
        {"value": "Receipt RCV-1 for 8,500 units", "source_name": "Delivery Receipt 1.txt"},
        {"value": "Receipt RCV-2 on September 17", "source_name": "Delivery Receipt 2.txt"}
    ]
    contradictions = ContradictionEngine.detect_contradictions(facts, [])
    
    assert len(contradictions) >= 2
    types = [c["contradiction_type"] for c in contradictions]
    assert "QUANTITY" in types
    assert "DATE" in types
