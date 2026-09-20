import pytest
from app.services.claim_engine import ClaimEngine

def test_claim_decomposition_dynamic_domains():
    # Test Domain 1: Medical Devices Procurement
    claim1 = "Company A delivered 10,000 medical devices to Hospital X before September 15."
    ac1 = ClaimEngine.decompose_claim(claim1)
    stmts1 = [a.statement for a in ac1]
    assert any("Company A" in s for s in stmts1)
    assert any("10,000" in s for s in stmts1)
    assert any("Hospital X" in s for s in stmts1)

    # Test Domain 2: Laptop IT Order (Completely Different Domain)
    claim2 = "Vendor Z supplied 2,000 laptops to University Y by March 1."
    ac2 = ClaimEngine.decompose_claim(claim2)
    stmts2 = [a.statement for a in ac2]
    assert any("Vendor Z" in s for s in stmts2)
    assert any("2,000" in s for s in stmts2)
    assert any("University Y" in s for s in stmts2)
    assert not any("Hospital X" in s for s in stmts2)  # Proves non-hardcoded behavior!

    # Test Domain 3: Construction Milestone Claim
    claim3 = "Subcontractor Alpha completed Phase 1 construction at Site Beta on August 30."
    ac3 = ClaimEngine.decompose_claim(claim3)
    stmts3 = [a.statement for a in ac3]
    assert any("Subcontractor Alpha" in s for s in stmts3)
    assert any("Site Beta" in s for s in stmts3)
