from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import datetime

# --- API Request Models ---
class CaseCreateRequest(BaseModel):
    title: str = Field(..., description="Short title for the case")
    claim_statement: str = Field(..., description="Main claim statement to investigate")
    mode: Optional[str] = Field("STANDARD", description="STANDARD, CHALLENGE, or RED_TEAM")

class ChallengeRequest(BaseModel):
    challenge_question: str = Field(..., description="Challenge statement or question to test against current conclusion")

class RedTeamRequest(BaseModel):
    target: Optional[str] = Field("TRY_TO_DISPROVE", description="Red team directive")

# --- Structured Outputs for AI Engines ---
class AtomicClaimSchema(BaseModel):
    statement: str
    subject: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    constraints: Dict[str, Any] = Field(default_factory=dict)
    verification_requirements: List[str] = Field(default_factory=list)

class ClaimDecompositionSchema(BaseModel):
    claim_id: str
    original_claim: str
    atomic_claims: List[AtomicClaimSchema]

class ExtractedFactSchema(BaseModel):
    value: str
    subject: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    page: int = 1
    source_span: Optional[str] = None
    extraction_method: str = "llm"
    confidence: float = 1.0

class EntityResolutionSchema(BaseModel):
    canonical_id: str
    entity_type: str
    display_name: str
    aliases: List[str] = Field(default_factory=list)
    confidence: float = 1.0

class EventExtractionSchema(BaseModel):
    event_type: str
    date_iso: Optional[str] = None  # YYYY-MM-DD
    display_date: str
    location: Optional[str] = None
    description: str
    is_deadline: bool = False

class ContradictionSchema(BaseModel):
    contradiction_type: str  # QUANTITY, DATE, LOCATION, IDENTITY, STATUS, SEQUENCE
    statement_a: str
    source_a: Optional[str] = None
    statement_b: str
    source_b: Optional[str] = None
    severity: str = "HIGH"
    status: str = "UNRESOLVED"

class HypothesisSchema(BaseModel):
    statement: str
    search_requirements: List[str] = Field(default_factory=list)

class EvidenceGapSchema(BaseModel):
    description: str
    why_it_matters: str
    next_best_evidence: str

class FinalAssessmentSchema(BaseModel):
    verdict: str  # SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, INSUFFICIENT_EVIDENCE, UNRESOLVED_CONFLICT
    reasoning: str
    direct_evidence_supported: bool
    independent_corroboration: bool
    temporal_consistency: bool
    numerical_consistency: bool
    major_conflicts: List[str] = Field(default_factory=list)
    missing_evidence_gaps: List[str] = Field(default_factory=list)

# --- Response Schemas ---
class AtomicClaimResponse(BaseModel):
    id: str
    statement: str
    subject: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    constraints_json: Dict[str, Any]
    verification_requirements_json: List[str]
    status: str
    confidence: float
    evidence_count: int
    contradiction_count: int

class SourceResponse(BaseModel):
    id: str
    name: str
    file_type: str
    source_type: str
    derived_from_source_id: Optional[str] = None
    created_at: datetime.datetime

class EventResponse(BaseModel):
    id: str
    event_type: str
    date_iso: Optional[str] = None
    display_date: str
    location: Optional[str] = None
    description: str
    is_deadline: bool
    source_name: Optional[str] = None

class ContradictionResponse(BaseModel):
    id: str
    contradiction_type: str
    statement_a: str
    source_a_name: Optional[str] = None
    statement_b: str
    source_b_name: Optional[str] = None
    severity: str
    status: str
    resolution_summary: Optional[str] = None

class HypothesisResponse(BaseModel):
    id: str
    contradiction_id: Optional[str] = None
    statement: str
    search_requirements_json: List[str]
    status: str
    findings: Optional[str] = None

class EvidenceGapResponse(BaseModel):
    id: str
    description: str
    why_it_matters: str
    next_best_evidence: str
    status: str

class InvestigationStepResponse(BaseModel):
    step_number: int
    step_type: str
    title: str
    detail: str
    timestamp: datetime.datetime

class CaseDetailResponse(BaseModel):
    id: str
    title: str
    claim_statement: str
    mode: str
    status: str
    verdict: Optional[str] = None
    verdict_reasoning: Optional[str] = None
    evidence_strength_json: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime
    atomic_claims: List[AtomicClaimResponse] = Field(default_factory=list)
    sources: List[SourceResponse] = Field(default_factory=list)
    events: List[EventResponse] = Field(default_factory=list)
    contradictions: List[ContradictionResponse] = Field(default_factory=list)
    hypotheses: List[HypothesisResponse] = Field(default_factory=list)
    evidence_gaps: List[EvidenceGapResponse] = Field(default_factory=list)
    steps: List[InvestigationStepResponse] = Field(default_factory=list)
