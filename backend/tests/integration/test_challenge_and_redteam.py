from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_challenge_and_redteam_endpoints():
    # 1. Load demo case
    load_res = client.post("/api/demo/load")
    assert load_res.status_code == 200
    case_data = load_res.json()
    case_id = case_data["id"]

    # 2. Challenge endpoint
    chal_res = client.post(f"/api/cases/{case_id}/challenge", json={
        "challenge_question": "Could remaining units have been delivered separately?"
    })
    assert chal_res.status_code == 200
    updated_case = chal_res.json()
    hypotheses_stmts = [h["statement"] for h in updated_case["hypotheses"]]
    assert any("Could remaining units have been delivered separately?" in s for s in hypotheses_stmts)

    # 3. Red-Team endpoint
    rt_res = client.post(f"/api/cases/{case_id}/red-team", json={"target": "TRY_TO_DISPROVE"})
    assert rt_res.status_code == 200
    rt_case = rt_res.json()
    assert rt_case["mode"] == "RED_TEAM"
    gaps_descs = [g["description"] for g in rt_case["evidence_gaps"]]
    assert any("RED TEAM" in d for d in gaps_descs)
