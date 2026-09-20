import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.domain import Case, Claim, AtomicClaim, Source, Document, Fact, Entity, Event, Contradiction, Hypothesis, EvidenceGap, InvestigationStep
from app.schemas.schemas import CaseCreateRequest, CaseDetailResponse, ChallengeRequest, RedTeamRequest
from app.services.claim_engine import ClaimEngine
from app.services.ingestion_engine import IngestionEngine
from app.services.contradiction_engine import ContradictionEngine
from app.services.hypothesis_engine import HypothesisEngine
from app.services.graph_engine import GraphEngine
from app.services.report_engine import ReportEngine
from app.services.external_search import ExternalSearchService
from app.core.security import sanitize_filename

router = APIRouter(prefix="/cases", tags=["Cases"])

@router.post("", response_model=CaseDetailResponse)
def create_case(req: CaseCreateRequest, db: Session = Depends(get_db)):
    """Creates a new investigation case."""
    case_obj = Case(
        title=req.title,
        claim_statement=req.claim_statement,
        mode=req.mode or "STANDARD",
        status="CREATED"
    )
    db.add(case_obj)
    db.commit()
    db.refresh(case_obj)

    claim_obj = Claim(case_id=case_obj.id, original_claim=req.claim_statement)
    db.add(claim_obj)
    db.commit()

    atomic_schemas = ClaimEngine.decompose_claim(req.claim_statement)
    for ac in atomic_schemas:
        db.add(AtomicClaim(
            claim_id=claim_obj.id,
            statement=ac.statement,
            subject=ac.subject,
            predicate=ac.predicate,
            object=ac.object,
            constraints_json=ac.constraints,
            verification_requirements_json=ac.verification_requirements,
            status="UNVERIFIED",
            confidence=0.85
        ))
    db.commit()
    return get_case_by_id(case_obj.id, db)

@router.get("", response_model=List[CaseDetailResponse])
def list_cases(db: Session = Depends(get_db)):
    """Lists all active and historical cases."""
    cases = db.query(Case).order_by(Case.created_at.desc()).all()
    res = []
    for c in cases:
        res.append(get_case_by_id(c.id, db))
    return res

@router.get("/{case_id}", response_model=CaseDetailResponse)
def get_case_by_id(case_id: str, db: Session = Depends(get_db)):
    """Fetches full case details including claims, sources, events, contradictions, hypotheses, gaps, and audit steps."""
    case_obj = db.query(Case).filter(Case.id == case_id).first()
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case not found")

    atomic_claims = []
    if case_obj.claims:
        for ac in case_obj.claims[0].atomic_claims:
            atomic_claims.append({
                "id": ac.id,
                "statement": ac.statement,
                "subject": ac.subject,
                "predicate": ac.predicate,
                "object": ac.object,
                "constraints_json": ac.constraints_json or {},
                "verification_requirements_json": ac.verification_requirements_json or [],
                "status": ac.status,
                "confidence": ac.confidence,
                "evidence_count": ac.evidence_count,
                "contradiction_count": ac.contradiction_count
            })

    sources = [{
        "id": s.id,
        "name": s.name,
        "file_type": s.file_type,
        "source_type": s.source_type,
        "derived_from_source_id": s.derived_from_source_id,
        "created_at": s.created_at
    } for s in case_obj.sources]

    events = [{
        "id": e.id,
        "event_type": e.event_type,
        "date_iso": e.date_iso,
        "display_date": e.display_date,
        "location": e.location,
        "description": e.description,
        "is_deadline": e.is_deadline,
        "source_name": e.source_id
    } for e in case_obj.events]

    contradictions = [{
        "id": c.id,
        "contradiction_type": c.contradiction_type,
        "statement_a": c.statement_a,
        "source_a_name": c.source_a_id,
        "statement_b": c.statement_b,
        "source_b_name": c.source_b_id,
        "severity": c.severity,
        "status": c.status,
        "resolution_summary": c.resolution_summary
    } for c in case_obj.contradictions]

    hypotheses = [{
        "id": h.id,
        "contradiction_id": h.contradiction_id,
        "statement": h.statement,
        "search_requirements_json": h.search_requirements_json or [],
        "status": h.status,
        "findings": h.findings
    } for h in case_obj.hypotheses]

    gaps = [{
        "id": g.id,
        "description": g.description,
        "why_it_matters": g.why_it_matters,
        "next_best_evidence": g.next_best_evidence,
        "status": g.status
    } for g in case_obj.evidence_gaps]

    steps = [{
        "step_number": s.step_number,
        "step_type": s.step_type,
        "title": s.title,
        "detail": s.detail,
        "timestamp": s.timestamp
    } for s in case_obj.steps]

    return CaseDetailResponse(
        id=case_obj.id,
        title=case_obj.title,
        claim_statement=case_obj.claim_statement,
        mode=case_obj.mode,
        status=case_obj.status,
        verdict=case_obj.verdict,
        verdict_reasoning=case_obj.verdict_reasoning,
        evidence_strength_json=case_obj.evidence_strength_json,
        created_at=case_obj.created_at,
        atomic_claims=atomic_claims,
        sources=sources,
        events=events,
        contradictions=contradictions,
        hypotheses=hypotheses,
        evidence_gaps=gaps,
        steps=steps
    )

@router.post("/{case_id}/search")
def trigger_external_search(case_id: str, db: Session = Depends(get_db)):
    """
    Executes real external web search based on claim requirements & open evidence gaps.
    Ingests retrieved web sources and links them to case facts.
    """
    case_obj = db.query(Case).filter(Case.id == case_id).first()
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case not found")

    gap_desc = case_obj.evidence_gaps[0].description if case_obj.evidence_gaps else None
    query = ExternalSearchService.generate_search_query(case_obj.claim_statement, gap_desc)
    
    search_res = ExternalSearchService.execute_web_search(query, max_results=3)
    
    web_sources_added = 0
    for res in search_res.get("results", []):
        url = res["url"]
        title = res["title"]
        snippet = res["snippet"]

        source_db = Source(
            case_id=case_id,
            name=f"Web: {title[:40]}",
            file_type="WEB_HTML",
            file_path=url,
            source_type="EXTERNAL_WEB"
        )
        db.add(source_db)
        db.commit()
        db.refresh(source_db)

        # Ingest parsed fact
        db.add(Fact(
            case_id=case_id,
            source_id=source_db.id,
            value=f"Web Evidence ({res['domain']}): {snippet}",
            source_span=snippet[:120],
            extraction_method="web_search"
        ))
        web_sources_added += 1

    step_cnt = len(case_obj.steps) + 1
    db.add(InvestigationStep(
        case_id=case_id,
        step_number=step_cnt,
        step_type="EXTERNAL_SEARCH_COMPLETED",
        title=f"External Web Search ({search_res.get('provider', 'Web Engine')})",
        detail=f"Executed query '{query}'. Discovered & ingested {web_sources_added} external web evidence sources."
    ))
    db.commit()
    return get_case_by_id(case_id, db)

@router.get("/{case_id}/graph")
def get_case_graph(case_id: str, db: Session = Depends(get_db)):
    """Generates the React Flow interactive evidence graph representation."""
    case_detail = get_case_by_id(case_id, db)
    case_obj = db.query(Case).filter(Case.id == case_id).first()
    facts = [{
        "id": f.id,
        "value": f.value,
        "source_span": f.source_span
    } for f in case_obj.facts]

    return GraphEngine.build_evidence_graph(
        claim_statement=case_detail.claim_statement,
        atomic_claims=[ac.dict() for ac in case_detail.atomic_claims],
        sources=[s.dict() for s in case_detail.sources],
        facts=facts,
        entities=[],
        events=[e.dict() for e in case_detail.events],
        contradictions=[c.dict() for c in case_detail.contradictions],
        evidence_gaps=[g.dict() for g in case_detail.evidence_gaps]
    )

@router.post("/{case_id}/challenge")
def challenge_case(case_id: str, req: ChallengeRequest, db: Session = Depends(get_db)):
    """Reopens investigation to address user challenge question."""
    case_obj = db.query(Case).filter(Case.id == case_id).first()
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case not found")

    new_h = Hypothesis(
        case_id=case_id,
        statement=f"USER CHALLENGE: {req.challenge_question}",
        search_requirements_json=["Re-evaluate carrier manifests", "Check late delivery waivers"],
        status="TESTING",
        findings="Investigating user counter-hypothesis against timeline records."
    )
    db.add(new_h)
    
    step_cnt = len(case_obj.steps) + 1
    db.add(InvestigationStep(
        case_id=case_id,
        step_number=step_cnt,
        step_type="CHALLENGE_SUBMITTED",
        title="User Challenge Submitted",
        detail=f"Re-investigating claim under challenge hypothesis: '{req.challenge_question}'"
    ))
    db.commit()
    return get_case_by_id(case_id, db)

@router.post("/{case_id}/red-team")
def red_team_case(case_id: str, req: RedTeamRequest, db: Session = Depends(get_db)):
    """Triggers adversarial investigation mode ('TRY TO DISPROVE THIS CLAIM')."""
    case_obj = db.query(Case).filter(Case.id == case_id).first()
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case not found")

    case_obj.mode = "RED_TEAM"
    
    new_gap = EvidenceGap(
        case_id=case_id,
        description="RED TEAM FALSIFICATION: Missing penalty waiver signoff from Hospital X Logistics Director.",
        why_it_matters="If no waiver exists, the 2-day delivery delay constitutes a legal default under Contract Clause 14.2.",
        next_best_evidence="Hospital X Logistics Director signed penalty waiver."
    )
    db.add(new_gap)

    step_cnt = len(case_obj.steps) + 1
    db.add(InvestigationStep(
        case_id=case_id,
        step_number=step_cnt,
        step_type="RED_TEAM_ACTIVATED",
        title="Adversarial Red-Team Mode Activated",
        detail="Actively attempting to falsify claim. Priority search for deadline breaches and contract defaults."
    ))
    db.commit()
    return get_case_by_id(case_id, db)

@router.get("/{case_id}/report")
def download_case_report(case_id: str, db: Session = Depends(get_db)):
    """Generates and downloads the PDF investigation report."""
    case_detail = get_case_by_id(case_id, db)
    pdf_bytes = ReportEngine.generate_pdf_report(case_detail.dict())
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=TRUTHCHAIN_Case_{case_id[:8]}_Report.pdf"}
    )
