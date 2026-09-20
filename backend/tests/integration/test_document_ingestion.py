import os
import pytest
from app.services.ingestion_engine import IngestionEngine
from app.demo.dataset_generator import generate_procurement_evidence, DATA_DIR

def test_multimodal_document_ingestion():
    generate_procurement_evidence()
    case_dir = os.path.join(DATA_DIR, "case_a_procurement")
    
    # Test TXT Ingestion
    txt_path = os.path.join(case_dir, "PO-2026-9042.txt")
    txt_docs = IngestionEngine.parse_file(txt_path, "PO-2026-9042.txt")
    assert len(txt_docs) == 1
    assert "10,000" in txt_docs[0]["raw_content"]

    # Test CSV Ingestion
    csv_path = os.path.join(case_dir, "Warehouse_Log_Sept14.csv")
    csv_docs = IngestionEngine.parse_file(csv_path, "Warehouse_Log_Sept14.csv")
    assert len(csv_docs) == 1
    assert "8470" in csv_docs[0]["raw_content"]

    # Test XLSX Ingestion
    xlsx_path = os.path.join(case_dir, "Final_Inventory_Ledger.xlsx")
    xlsx_docs = IngestionEngine.parse_file(xlsx_path, "Final_Inventory_Ledger.xlsx")
    assert len(xlsx_docs) >= 1
    assert "10000" in xlsx_docs[0]["raw_content"] or "10,000" in xlsx_docs[0]["raw_content"]
