import pytest
from app.services.external_search import ExternalSearchService

def test_generate_search_query():
    claim = "Company A delivered 10,000 medical devices to Hospital X before September 15."
    gap = "Missing official shipping receipt."
    
    query = ExternalSearchService.generate_search_query(claim, gap)
    assert isinstance(query, str)
    assert len(query) > 0
    assert "Company" in query or "Hospital" in query or "10000" in query or "shipping" in query

def test_execute_web_search():
    query = "Medical device delivery compliance regulations"
    res = ExternalSearchService.execute_web_search(query, max_results=2)
    
    assert "status" in res
    assert "provider" in res
    assert "query" in res
    assert "results" in res
    assert res["status"] in ["ACTIVE", "QUOTA_EXHAUSTED", "TEMPORARILY_UNAVAILABLE"]
    assert isinstance(res["results"], list)

def test_fetch_page_content_invalid_url():
    assert ExternalSearchService.fetch_page_content(None) is None
    assert ExternalSearchService.fetch_page_content("invalid-url") is None
