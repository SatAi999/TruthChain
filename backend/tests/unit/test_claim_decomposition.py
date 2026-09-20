import pytest
from app.services.claim_engine import ClaimEngine

def test_claim_decomposition_procurement():
    claim = "Company A delivered 10,000 medical devices to Hospital X before September 15."
    atomic_claims = ClaimEngine.decompose_claim(claim)
    
    assert len(atomic_claims) >= 3
    statements = [ac.statement for ac in atomic_claims]
    assert any("Company A" in s or "delivered" in s for s in statements)
    assert any("Hospital X" in s or "Hospital" in s for s in statements)
