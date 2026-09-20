import datetime
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    claim_statement = Column(Text, nullable=False)
    mode = Column(String, default="STANDARD")  # STANDARD, CHALLENGE, RED_TEAM
    status = Column(String, default="CREATED")  # CREATED, INVESTIGATING, COMPLETED, ERROR
    verdict = Column(String, nullable=True)  # SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, INSUFFICIENT_EVIDENCE, UNRESOLVED_CONFLICT
    verdict_reasoning = Column(Text, nullable=True)
    evidence_strength_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    claims = relationship("Claim", back_populates="case", cascade="all, delete-orphan")
    sources = relationship("Source", back_populates="case", cascade="all, delete-orphan")
    facts = relationship("Fact", back_populates="case", cascade="all, delete-orphan")
    entities = relationship("Entity", back_populates="case", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="case", cascade="all, delete-orphan")
    contradictions = relationship("Contradiction", back_populates="case", cascade="all, delete-orphan")
    hypotheses = relationship("Hypothesis", back_populates="case", cascade="all, delete-orphan")
    evidence_gaps = relationship("EvidenceGap", back_populates="case", cascade="all, delete-orphan")
    steps = relationship("InvestigationStep", back_populates="case", cascade="all, delete-orphan")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    original_claim = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    case = relationship("Case", back_populates="claims")
    atomic_claims = relationship("AtomicClaim", back_populates="claim", cascade="all, delete-orphan")


class AtomicClaim(Base):
    __tablename__ = "atomic_claims"

    id = Column(String, primary_key=True, default=generate_uuid)
    claim_id = Column(String, ForeignKey("claims.id", ondelete="CASCADE"), nullable=False)
    statement = Column(Text, nullable=False)
    subject = Column(String, nullable=True)
    predicate = Column(String, nullable=True)
    object = Column(String, nullable=True)
    constraints_json = Column(JSON, default=dict)
    verification_requirements_json = Column(JSON, default=list)
    status = Column(String, default="UNVERIFIED")  # SUPPORTED, CONTRADICTED, PARTIAL, UNVERIFIED
    confidence = Column(Float, default=0.0)
    evidence_count = Column(Integer, default=0)
    contradiction_count = Column(Integer, default=0)

    claim = relationship("Claim", back_populates="atomic_claims")


class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    source_type = Column(String, default="PRIMARY")  # PRIMARY, DERIVED, COPIED
    derived_from_source_id = Column(String, nullable=True)
    content_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    case = relationship("Case", back_populates="sources")
    documents = relationship("Document", back_populates="source", cascade="all, delete-orphan")
    facts = relationship("Fact", back_populates="source", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_id = Column(String, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    page_number = Column(Integer, default=1)
    section_name = Column(String, nullable=True)
    raw_content = Column(Text, nullable=False)

    source = relationship("Source", back_populates="documents")


class Fact(Base):
    __tablename__ = "facts"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    page = Column(Integer, default=1)
    value = Column(Text, nullable=False)
    subject = Column(String, nullable=True)
    predicate = Column(String, nullable=True)
    object = Column(String, nullable=True)
    source_span = Column(Text, nullable=True)
    extraction_method = Column(String, default="llm")  # llm, regex, parser, ocr
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    case = relationship("Case", back_populates="facts")
    source = relationship("Source", back_populates="facts")


class Entity(Base):
    __tablename__ = "entities"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    canonical_id = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)  # PERSON, ORGANIZATION, LOCATION, PRODUCT, ORDER, INVOICE, SHIPMENT, CONTRACT, EVENT
    display_name = Column(String, nullable=False)
    aliases_json = Column(JSON, default=list)
    confidence = Column(Float, default=1.0)

    case = relationship("Case", back_populates="entities")


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    fact_id = Column(String, ForeignKey("facts.id", ondelete="SET NULL"), nullable=True)
    event_type = Column(String, nullable=False)
    date_iso = Column(String, nullable=True)  # YYYY-MM-DD
    display_date = Column(String, nullable=False)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    is_deadline = Column(Boolean, default=False)
    verified = Column(Boolean, default=True)

    case = relationship("Case", back_populates="events")


class EvidenceLink(Base):
    __tablename__ = "evidence_links"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    target_type = Column(String, nullable=False)  # ATOMIC_CLAIM, FACT, ENTITY, CONTRADICTION
    target_id = Column(String, nullable=False)
    link_type = Column(String, nullable=False)  # SUPPORTS, CONTRADICTS, DERIVED_FROM, MENTIONS, CORROBORATES
    reasoning = Column(Text, nullable=True)


class Contradiction(Base):
    __tablename__ = "contradictions"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    contradiction_type = Column(String, nullable=False)  # QUANTITY, DATE, LOCATION, IDENTITY, STATUS, SEQUENCE
    statement_a = Column(Text, nullable=False)
    source_a_id = Column(String, nullable=True)
    statement_b = Column(Text, nullable=False)
    source_b_id = Column(String, nullable=True)
    severity = Column(String, default="HIGH")  # HIGH, MEDIUM, LOW
    status = Column(String, default="UNRESOLVED")  # UNRESOLVED, RESOLVED, DISPROVED
    resolution_summary = Column(Text, nullable=True)

    case = relationship("Case", back_populates="contradictions")
    hypotheses = relationship("Hypothesis", back_populates="contradiction", cascade="all, delete-orphan")


class Hypothesis(Base):
    __tablename__ = "hypotheses"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    contradiction_id = Column(String, ForeignKey("contradictions.id", ondelete="CASCADE"), nullable=True)
    statement = Column(Text, nullable=False)
    search_requirements_json = Column(JSON, default=list)
    status = Column(String, default="TESTING")  # TESTING, CONFIRMED, DISPROVED, INCONCLUSIVE
    findings = Column(Text, nullable=True)

    case = relationship("Case", back_populates="hypotheses")
    contradiction = relationship("Contradiction", back_populates="hypotheses")


class EvidenceGap(Base):
    __tablename__ = "evidence_gaps"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    claim_id = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    why_it_matters = Column(Text, nullable=False)
    next_best_evidence = Column(Text, nullable=False)
    status = Column(String, default="OPEN")  # OPEN, RESOLVED

    case = relationship("Case", back_populates="evidence_gaps")


class InvestigationStep(Base):
    __tablename__ = "investigation_steps"

    id = Column(String, primary_key=True, default=generate_uuid)
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    step_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    detail = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="DONE")

    case = relationship("Case", back_populates="steps")
