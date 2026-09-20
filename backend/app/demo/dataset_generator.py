import os
import csv
import json
import openpyxl

DEMO_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DEMO_DIR, "data")
EXPECTED_DIR = os.path.join(DEMO_DIR, "expected_results")

def generate_procurement_evidence():
    """Generates the 13 evidence files for Case A (Procurement Investigation)."""
    os.makedirs(os.path.join(DATA_DIR, "case_a_procurement"), exist_ok=True)
    case_dir = os.path.join(DATA_DIR, "case_a_procurement")

    # 1. Purchase Order
    po_content = """PURCHASE ORDER: PO-2026-9042
Date: September 10, 2026
Buyer: Hospital X Medical Center (Receiving Site X)
Vendor: Company A Technologies Ltd (Supplier A)
Contract Ref: Master Supply Agreement MSA-2025-09

Line Items:
Item 1: Medical Devices (Catalog #MD-10K) - Quantity: 10,000 units
Unit Price: $150.00 | Total: $1,500,000.00

Special Delivery Term:
CRITICAL DEADLINE: All 10,000 medical devices must be delivered in full to Hospital X receiving dock prior to 5:00 PM on September 15, 2026.
Late delivery subject to 5% penalty per calendar day delay as per Master Agreement Clause 14.2.
"""
    with open(os.path.join(case_dir, "PO-2026-9042.txt"), "w", encoding="utf-8") as f:
        f.write(po_content)

    # 2. Master Contract
    contract_content = """MASTER SUPPLY AGREEMENT (MSA-2025-09)
Between: Company A Technologies Ltd ("Supplier") and Hospital X Health System ("Buyer")

Section 4.1 - Delivery & Completion:
A delivery obligation is considered fulfilled only upon physical receipt and intake verification of the full quantity specified in the active Purchase Order at Buyer's designated facility.

Section 14.2 - Penalties for Late Delivery:
If Supplier fails to deliver 100% of the ordered quantity on or before the Purchase Order Deadline Date (September 15, 2026 for PO-2026-9042), Buyer reserves the right to withhold 5% of order invoice value per day until final balance is received.
"""
    with open(os.path.join(case_dir, "Master_Supply_Contract.txt"), "w", encoding="utf-8") as f:
        f.write(contract_content)

    # 3. Vendor Invoice
    inv_content = """COMMERCIAL INVOICE: INV-8821
Invoice Date: September 11, 2026
Bill To: Hospital X Medical Center
From: Company A Technologies Ltd

Purchase Order Ref: PO-2026-9042
Description: 10,000 Medical Devices (Catalog #MD-10K)
Billed Quantity: 10,000 units
Total Amount Due: $1,500,000.00
Payment Terms: Net 30 days upon full delivery verification.
"""
    with open(os.path.join(case_dir, "INV-8821.txt"), "w", encoding="utf-8") as f:
        f.write(inv_content)

    # 4. Carrier Bill of Lading #1
    bol1_content = """CARRIER BILL OF LADING: BOL-5541
Carrier: Apex Logistics Corp
Dispatch Date: September 12, 2026
Shipper: Company A Manufacturing Facility
Consignee: Hospital X Medical Center, Receiving Dock B

Manifest Details:
Shipment #1 of PO-2026-9042
Container ID: APX-9921
Quantity Dispatched: 8,500 units of Medical Device #MD-10K
Pallet Count: 170 pallets
Status: In Transit - Scheduled Receipt Sept 14, 2026.
"""
    with open(os.path.join(case_dir, "Carrier_BOL_5541.txt"), "w", encoding="utf-8") as f:
        f.write(bol1_content)

    # 5. Hospital Receiving Receipt #1
    rcpt1_content = """HOSPITAL X RECEIVING DOCK LOG
Receipt ID: RCV-2026-0914-A
Date Received: September 14, 2026 (Time: 14:15 EST)
Carrier: Apex Logistics Corp (BOL-5541)
Purchase Order: PO-2026-9042

Inspection Record:
Items Delivered: Medical Devices #MD-10K
Quantity Counted at Dock: 8,500 units
Intake Note: First partial delivery of 8,500 units accepted into holding area. 1,500 units remaining outstanding on PO.
Received By: J. Miller, Dock Logistics Officer.
"""
    with open(os.path.join(case_dir, "Hospital_Receiving_Receipt_1.txt"), "w", encoding="utf-8") as f:
        f.write(rcpt1_content)

    # 6. Warehouse Log CSV
    wh_csv_path = os.path.join(case_dir, "Warehouse_Log_Sept14.csv")
    with open(wh_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Log_ID", "PO_Ref", "Item_Code", "Received_Qty", "Accepted_Qty", "Damaged_Qty", "Notes"])
        writer.writerow(["2026-09-14", "WH-8820", "PO-2026-9042", "MD-10K", "8500", "8470", "30", "30 units flagged with torn outer packaging"])

    # 7. Supplier Email regarding backorder
    email_content = """From: logistics@companya.com
To: procurement@hospitalx.org
Date: September 15, 2026 09:30 AM
Subject: Update regarding PO-2026-9042 remaining balance

Dear Hospital X Logistics Team,

Please be advised that due to a temporary component backorder at our primary assembly line, Shipment #1 dispatched on Sept 12 contained 8,500 units out of the total 10,000 ordered on PO-2026-9042.

The remaining 1,500 units have been fully assembled and tested. They are scheduled for express dispatch via Swift Express today, September 16, and will arrive at Hospital X on September 17, 2026.

We apologize for the 2-day delay on the remaining balance.

Best regards,
Logistics Team, Company A
"""
    with open(os.path.join(case_dir, "Supplier_Email_Backorder.txt"), "w", encoding="utf-8") as f:
        f.write(email_content)

    # 8. Carrier Manifest #2
    manifest2_content = """CARRIER MANIFEST: SWIFT-7714
Carrier: Swift Express Freight
Dispatch Date: September 16, 2026
Shipper: Company A Technologies Ltd
Consignee: Hospital X Medical Center

Shipment #2 of PO-2026-9042 (Final Balance)
Quantity Dispatched: 1,500 units of Medical Device #MD-10K
Tracking Number: SWF-1,500-FINAL
Destination Arrival: September 17, 2026.
"""
    with open(os.path.join(case_dir, "Carrier_Manifest_Shipment2.txt"), "w", encoding="utf-8") as f:
        f.write(manifest2_content)

    # 9. Hospital Receiving Receipt #2
    rcpt2_content = """HOSPITAL X RECEIVING DOCK LOG
Receipt ID: RCV-2026-0917-B
Date Received: September 17, 2026 (Time: 10:30 AM EST)
Carrier: Swift Express Freight (SWIFT-7714)
Purchase Order: PO-2026-9042

Inspection Record:
Items Delivered: Medical Devices #MD-10K (Final Shipment)
Quantity Counted at Dock: 1,500 units
Intake Note: Second delivery of 1,500 units accepted. Total PO accumulation now reaches 10,000 units.
Note on Date: Full order completion achieved on Sept 17 (2 days past PO deadline of Sept 15).
Received By: J. Miller, Dock Logistics Officer.
"""
    with open(os.path.join(case_dir, "Hospital_Receiving_Receipt_2.txt"), "w", encoding="utf-8") as f:
        f.write(rcpt2_content)

    # 10. Final Inventory Ledger XLSX
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory Ledger"
    ws.append(["Batch_ID", "PO_Reference", "Receipt_Date", "Quantity", "Location", "Audit_Status"])
    ws.append(["BATCH-01", "PO-2026-9042", "2026-09-14", 8500, "Hospital X - Dock B", "AUDITED"])
    ws.append(["BATCH-02", "PO-2026-9042", "2026-09-17", 1500, "Hospital X - Dock B", "AUDITED"])
    ws.append(["TOTAL", "PO-2026-9042", "COMBINED", 10000, "Hospital X Central Warehouse", "VERIFIED COMPLETE"])
    wb.save(os.path.join(case_dir, "Final_Inventory_Ledger.xlsx"))

    # 11. Derived News Article (Lineage test)
    news_content = """TECH HEALTH JOURNAL (Sept 18, 2026):
Company A Technologies today announced the successful delivery of 10,000 medical devices to Hospital X under order PO-2026-9042.
(Source Note: Article rewritten from Company A press release published Sept 17).
"""
    with open(os.path.join(case_dir, "Derived_News_Snippet.txt"), "w", encoding="utf-8") as f:
        f.write(news_content)


def generate_additional_test_cases():
    """Generates evidence files for Cases B, C, D, E."""
    # Case B - Timeline
    case_b_dir = os.path.join(DATA_DIR, "case_b_timeline")
    os.makedirs(case_b_dir, exist_ok=True)
    with open(os.path.join(case_b_dir, "Board_Minutes_March12.txt"), "w") as f:
        f.write("Board Meeting held March 12, 2026 at 14:00. Executive Y attended via Zoom from London.")
    with open(os.path.join(case_b_dir, "Flight_Manifest_March12.txt"), "w") as f:
        f.write("Flight BA-178 departing London to NYC at 13:30 March 12, 2026. Passenger: Executive Y.")

    # Case C - Entity Resolution
    case_c_dir = os.path.join(DATA_DIR, "case_c_entity")
    os.makedirs(case_c_dir, exist_ok=True)
    with open(os.path.join(case_c_dir, "SEC_Filing.txt"), "w") as f:
        f.write("TechCorp Inc. (formerly Tech Corp LLC) announced acquisition of CyberSoft Solutions Ltd (also known as CS Solutions).")

    # Case D - Contradiction
    case_d_dir = os.path.join(DATA_DIR, "case_d_contradiction")
    os.makedirs(case_d_dir, exist_ok=True)
    with open(os.path.join(case_d_dir, "Subcontractor_Report.txt"), "w") as f:
        f.write("Subcontractor Z completed 100% of Phase 1 milestone on August 30.")
    with open(os.path.join(case_d_dir, "Site_Inspector_Audit.txt"), "w") as f:
        f.write("Site audit on Sept 2 indicates Phase 1 milestone only 60% complete.")

    # Case E - Red-Team Mode
    case_e_dir = os.path.join(DATA_DIR, "case_e_redteam")
    os.makedirs(case_e_dir, exist_ok=True)
    with open(os.path.join(case_e_dir, "Initial_Lab_Certificate.txt"), "w") as f:
        f.write("Product Beta passed safety tests on July 10, 2026.")
    with open(os.path.join(case_e_dir, "Internal_QA_Flag_Memo.txt"), "w") as f:
        f.write("CONFIDENTIAL QA MEMO: Product Beta failed re-testing on August 5 due to voltage instability.")


def generate_expected_results():
    """Generates expected assertion files for automated tests."""
    os.makedirs(EXPECTED_DIR, exist_ok=True)

    expected_case_a = {
        "case_id": "case_a_procurement",
        "claim": "Company A delivered 10,000 medical devices to Hospital X before September 15.",
        "expected_verdict": "PARTIALLY_SUPPORTED",
        "expected_atomic_claims": [
            "Company A is the contracted supplier",
            "Total ordered quantity is 10,000 units",
            "Delivery occurred at Hospital X",
            "Total delivered quantity is 10,000 units",
            "Full delivery requirement before September 15"
        ],
        "expected_delivered_total": 10000,
        "expected_shipment_count": 2,
        "expected_contradictions": [
            {"type": "QUANTITY", "status": "RESOLVED"},
            {"type": "DATE", "status": "UNRESOLVED"}
        ],
        "expected_deadline_violated": True,
        "expected_days_late": 2
    }

    with open(os.path.join(EXPECTED_DIR, "case_a_expected.json"), "w", encoding="utf-8") as f:
        json.dump(expected_case_a, f, indent=2)


if __name__ == "__main__":
    generate_procurement_evidence()
    generate_additional_test_cases()
    generate_expected_results()
    print("Demo dataset & expected results generated successfully.")
