import pytest
from app.services.independence_engine import SourceIndependenceEngine

def test_source_lineage_analysis():
    sources = [
        {"name": "Supplier_Email.txt", "source_type": "PRIMARY"},
        {"name": "Invoice.txt", "source_type": "PRIMARY"},
        {"name": "News_Article_Derived.txt", "source_type": "DERIVED", "derived_from_source_id": "Supplier_Email.txt"}
    ]

    res = SourceIndependenceEngine.analyze_lineage(sources)
    assert res["total_sources"] == 3
    assert len(res["independent_primary_sources"]) == 2
    assert len(res["derived_or_copied_sources"]) == 1
    assert res["independence_ratio"] == 0.67
