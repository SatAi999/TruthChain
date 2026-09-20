import os
import sys
from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.models.domain import Case, Claim, AtomicClaim, Source, Document, Fact, Entity, Event, Contradiction, Hypothesis, EvidenceGap, InvestigationStep
from app.demo.dataset_generator import generate_procurement_evidence, generate_additional_test_cases, generate_expected_results, DATA_DIR
from app.services.ingestion_engine import IngestionEngine
from app.services.claim_engine import ClaimEngine
from app.services.temporal_engine import TemporalEngine
from app.services.numerical_engine import NumericalEngine
from app.services.contradiction_engine import ContradictionEngine
from app.services.hypothesis_engine import HypothesisEngine

def seed_procurement_demo_case(db: Session) -> Case:
    """
    Seeds Case A (Procurement Investigation) idempotently into the database.
    """
    case_title = "Procurement Investigation — Company A 10,000 Units"
    existing_case = db.query(Case).filter(Case.title == case_title).first()
    if existing_case:
        print(f"Demo case '{case_title}' already exists (ID: {existing_case.id}). Skipping re-seed.")
        return existing_case

    # Make sure evidence dataset files exist on disk
    generate_procurement_evidence()
    generate_additional_test_cases()
    generate_expected_results()

    claim_stmt = "Company A delivered 10,000 medical devices to Hospital X before September 15."

    new_case = Case(
        title=case_title,
        claim_statement=claim_stmt,
        mode="STANDARD",
        status="INVESTIGATING"
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    # 1. Claim & Atomic Claims
    main_claim = Claim(case_id=new_case.id, original_claim=claim_stmt)
    db.add(main_claim)
    db.commit()

    atomic_schemas = ClaimEngine.decompose_claim(claim_stmt)
    for ac in atomic_schemas:
        atomic_db = AtomicClaim(
            claim_id=main_claim.id,
            statement=ac.statement,
            subject=ac.subject,
            predicate=ac.predicate,
            object=ac.object,
            constraints_json=ac.constraints,
            verification_requirements_json=ac.verification_requirements,
            status="UNVERIFIED",
            confidence=0.9
        )
        db.add(atomic_db)

    # 2. Ingest Evidence Files
    case_a_dir = os.path.join(DATA_DIR, "case_a_procurement")
    files = sorted(os.listdir(case_a_dir))
    
    facts_extracted = []
    events_extracted = []
    sources_db_map = {}

    for idx, fname in enumerate(files, start=1):
        fpath = os.path.join(case_a_dir, fname)
        ext = os.path.splitext(fname)[1].lower()
        stype = "DERIVED" if "Derived" in fname else "PRIMARY"

        source_db = Source(
            case_id=new_case.id,
            name=fname,
            file_type=ext.replace(".", "").upper(),
            file_path=fpath,
            source_type=stype
        )
        db.add(source_db)
        db.commit()
        db.refresh(source_db)
        sources_db_map[fname] = source_db

        parsed_docs = IngestionEngine.parse_file(fpath, fname)
        for doc_item in parsed_docs:
            doc_db = Document(
                source_id=source_db.id,
                page_number=doc_item["page_number"],
                section_name=doc_item["section_name"],
                raw_content=doc_item["raw_content"]
            )
            db.add(doc_db)
            db.commit()

            # Fact Extraction Simulation / Parsing
            val_text = doc_item["raw_content"][:250].replace("\n", " ")
            fact_db = Fact(
                case_id=new_case.id,
                source_id=source_db.id,
                document_id=doc_db.id,
                page=doc_item["page_number"],
                value=val_text,
                source_span=val_text[:100],
                extraction_method="parser"
            )
            db.add(fact_db)
            facts_extracted.append({"value": val_text, "source_name": fname})

            # Event Extraction
            if "PO-2026-9042" in fname:
                events_extracted.append(Event(
                    case_id=new_case.id,
                    source_id=source_db.id,
                    event_type="PO_ISSUED",
                    date_iso="2026-09-10",
                    display_date="10 Sep 2026",
                    location="Hospital X Dock",
                    description="PO-2026-9042 issued for 10,000 units with Sept 15 deadline."
                ))
                events_extracted.append(Event(
                    case_id=new_case.id,
                    source_id=source_db.id,
                    event_type="CONTRACT_DEADLINE",
                    date_iso="2026-09-15",
                    display_date="15 Sep 2026",
                    location="Hospital X Receiving Dock",
                    description="Mandatory delivery deadline for 100% of order balance.",
                    is_deadline=True
                ))
            elif "BOL_5541" in fname:
                events_extracted.append(Event(
                    case_id=new_case.id,
                    source_id=source_db.id,
                    event_type="SHIPMENT_DISPATCH",
                    date_iso="2026-09-12",
                    display_date="12 Sep 2026",
                    location="Company A Plant",
                    description="First shipment of 8,500 units dispatched via Apex Logistics."
                ))
            elif "Hospital_Receiving_Receipt_1" in fname:
                events_extracted.append(Event(
                    case_id=new_case.id,
                    source_id=source_db.id,
                    event_type="PARTIAL_DELIVERY",
                    date_iso="2026-09-14",
                    display_date="14 Sep 2026",
                    location="Hospital X Dock B",
                    description="First delivery of 8,500 units received and logged."
                ))
            elif "Supplier_Email_Backorder" in fname:
                events_extracted.append(Event(
                    case_id=new_case.id,
                    source_id=source_db.id,
                    event_type="BACKORDER_NOTICE",
                    date_iso="2026-09-15",
                    display_date="15 Sep 2026",
                    location="Company A Logistics",
                    description="Supplier notice confirming 1,500 unit balance backorder dispatch."
                ))
            elif "Hospital_Receiving_Receipt_2" in fname:
                events_extracted.append(Event(
                    case_id=new_case.id,
                    source_id=source_db.id,
                    event_type="FINAL_DELIVERY",
                    date_iso="2026-09-17",
                    display_date="17 Sep 2026",
                    location="Hospital X Dock B",
                    description="Second delivery of 1,500 units received (Order total complete 10,000)."
                ))

    for ev in events_extracted:
        db.add(ev)

    # 3. Contradictions & Agentic Hypothesis Loop
    raw_contradictions = ContradictionEngine.detect_contradictions(facts_extracted, [])
    for c in raw_contradictions:
        c_db = Contradiction(
            case_id=new_case.id,
            contradiction_type=c["contradiction_type"],
            statement_a=c["statement_a"],
            source_a_id=c.get("source_a_name"),
            statement_b=c["statement_b"],
            source_b_id=c.get("source_b_name"),
            severity=c["severity"],
            status=c["status"],
            resolution_summary=c.get("resolution_summary")
        )
        db.add(c_db)

    hyp_gap_res = HypothesisEngine.generate_hypotheses_and_gaps(raw_contradictions, facts_extracted)
    for h in hyp_gap_res["hypotheses"]:
        h_db = Hypothesis(
            case_id=new_case.id,
            statement=h["statement"],
            search_requirements_json=h["search_requirements"],
            status=h["status"],
            findings=h.get("findings")
        )
        db.add(h_db)

    for g in hyp_gap_res["evidence_gaps"]:
        g_db = EvidenceGap(
            case_id=new_case.id,
            description=g["description"],
            why_it_matters=g["why_it_matters"],
            next_best_evidence=g["next_best_evidence"]
        )
        db.add(g_db)

    # 4. Final Verdict & Audit Trail Steps
    new_case.status = "COMPLETED"
    new_case.verdict = "PARTIALLY_SUPPORTED"
    new_case.verdict_reasoning = (
        "Evidence confirms that 10,000 medical devices were eventually delivered to Hospital X "
        "(8,500 units received on Sept 14 + 1,500 units received on Sept 17). However, the evidence "
        "CONTRADICTS the claim requirement that all 10,000 units were delivered BEFORE September 15."
    )
    new_case.evidence_strength_json = {
        "direct_evidence": True,
        "independent_corroboration": True,
        "temporal_consistency": False,
        "numerical_consistency": True,
        "confidence_score": 0.88
    }

    steps = [
        ("CLAIM_DECOMPOSED", "Claim Decomposed", "Original claim split into 5 verifiable atomic propositions."),
        ("SOURCE_INGESTION", "Ingested Evidence Package", f"Processed {len(files)} evidence documents across PDF, CSV, XLSX, and TXT."),
        ("FACT_EXTRACTION", "Extracted 43 Facts & Entities", "Resolved entities 'Company A' and 'Hospital X' with canonical IDs."),
        ("CONTRADICTION_DETECTED", "Discrepancies Flagged", "Detected quantity mismatch between PO and first receipt, and Sept 17 deadline violation."),
        ("HYPOTHESIS_RESOLVED", "Second Shipment Confirmed", "Discovered Supplier Email & Carrier Manifest #2 confirming 1,500 units delivered Sept 17."),
        ("TIMELINE_RECONSTRUCTED", "Timeline Reconstructed", "Determined complete event timeline from Sept 10 PO to Sept 17 final receipt."),
        ("VERDICT_GENERATED", "Verdict Established", "Final assessment: PARTIALLY_SUPPORTED (10,000 units received, Sept 15 deadline failed).")
    ]

    for idx, (stype, title, detail) in enumerate(steps, start=1):
        db.add(InvestigationStep(
            case_id=new_case.id,
            step_number=idx,
            step_type=stype,
            title=title,
            detail=detail
        ))

    db.commit()
    db.refresh(new_case)
    print(f"Successfully seeded demo case '{case_title}' (ID: {new_case.id}).")
    return new_case

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_procurement_demo_case(db)
    finally:
        db.close()
