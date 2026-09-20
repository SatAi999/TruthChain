import pytest
from app.services.hypothesis_engine import HypothesisEngine
from app.services.contradiction_engine import ContradictionEngine

def test_hypothesis_generation_is_dynamic():
    # Case 1: Unresolved Quantity Contradiction without second shipment
    contradiction_unresolved = [{
        "contradiction_type": "QUANTITY",
        "statement_a": "PO requires 10,000 units",
        "statement_b": "Receipt 1 records 8,500 units",
        "severity": "HIGH",
        "status": "UNRESOLVED"
    }]
    facts_no_shipment2 = [
        {"value": "PO-9042 for 10,000 units", "source_name": "PO.txt"},
        {"value": "Delivery 1 for 8,500 units", "source_name": "Receipt1.txt"}
    ]

    res1 = HypothesisEngine.generate_hypotheses_and_gaps(contradiction_unresolved, facts_no_shipment2)
    assert len(res1["hypotheses"]) >= 1
    assert res1["hypotheses"][0]["status"] == "TESTING"
    assert len(res1["evidence_gaps"]) >= 1

    # Case 2: Resolved Quantity Contradiction with second shipment
    facts_with_shipment2 = [
        {"value": "PO-9042 for 10,000 units", "source_name": "PO.txt"},
        {"value": "Delivery 1 for 8,500 units", "source_name": "Receipt1.txt"},
        {"value": "Delivery 2 for 1,500 units", "source_name": "Hospital_Receiving_Receipt_2.txt"}
    ]
    res2 = HypothesisEngine.generate_hypotheses_and_gaps(contradiction_unresolved, facts_with_shipment2)
    assert res2["hypotheses"][0]["status"] == "CONFIRMED"
