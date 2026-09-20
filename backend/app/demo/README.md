# TRUTHCHAIN Demo Datasets & Test Scenarios

This directory contains reproducible test cases and dataset loaders for TRUTHCHAIN.

## Test Scenarios Overview

### Case A — Procurement Investigation (Primary Demo)
- **Claim**: *"Company A delivered 10,000 medical devices to Hospital X before September 15."*
- **Included Evidence (11 files)**:
  - `PO-2026-9042.txt` (PO for 10,000 units, Sept 10, deadline Sept 15)
  - `Master_Supply_Contract.txt` (Contract terms: Full delivery completion required)
  - `INV-8821.txt` (Invoice for 10,000 units, Sept 11)
  - `Carrier_BOL_5541.txt` (Carrier BOL #1: 8,500 units shipped Sept 12)
  - `Hospital_Receiving_Receipt_1.txt` (Receipt #1: 8,500 units received Sept 14)
  - `Warehouse_Log_Sept14.csv` (Warehouse Intake: 8,470 accepted, 30 damaged)
  - `Supplier_Email_Backorder.txt` (Email Sept 15: Remaining 1,500 units dispatched Sept 16)
  - `Carrier_Manifest_Shipment2.txt` (Carrier Manifest #2: 1,500 units shipped Sept 16)
  - `Hospital_Receiving_Receipt_2.txt` (Receipt #2: 1,500 units received Sept 17)
  - `Final_Inventory_Ledger.xlsx` (Inventory audit: 10,000 total received)
  - `Derived_News_Snippet.txt` (Derived news snippet - lineage test)
- **Expected Outcome**:
  - Total units delivered = $8,500 + 1,500 = 10,000$ (Numerical engine supported)
  - Full delivery date = September 17 (Temporal engine deadline violation vs Sept 15)
  - **Verdict**: `PARTIALLY_SUPPORTED` / `CONTRADICTED` deadline.

### Case B — Timeline Investigation
- Tests chronological ordering, date parsing, missing intervals, and sequence contradictions.

### Case C — Entity Resolution
- Tests alias canonicalization ("Company A Ltd", "Company A Technologies", "Supplier A" -> `ENT_COMPANY_A`).

### Case D — Contradiction Investigation
- Tests quantity discrepancies between subcontractor progress reports vs site inspector audit logs.

### Case E — Red-Team Mode
- Tests adversarial falsification searching for hidden internal QA defect memos overriding initial lab certificates.

## Running Dataset Loader & Seeder

```bash
# Generate evidence files and expected test results
python -m app.demo.dataset_generator

# Idempotently seed database with Case A
python -m app.demo.seed
```

Or trigger endpoint via HTTP API:
```http
POST /api/demo/load
```
