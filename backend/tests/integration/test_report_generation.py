from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pdf_report_download():
    # Load demo case
    load_res = client.post("/api/demo/load")
    case_id = load_res.json()["id"]

    report_res = client.get(f"/api/cases/{case_id}/report")
    assert report_res.status_code == 200
    assert report_res.headers["content-type"] == "application/pdf"
    assert len(report_res.content) > 1000
    assert report_res.content.startswith(b"%PDF")
