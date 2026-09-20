import pytest
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.demo.seed import seed_procurement_demo_case
from app.models.domain import Case

def test_full_demo_investigation_e2e():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        demo_case = seed_procurement_demo_case(db)
        assert demo_case is not None
        assert demo_case.verdict == "PARTIALLY_SUPPORTED"
        assert len(demo_case.sources) >= 10
        assert len(demo_case.contradictions) >= 2
        assert len(demo_case.events) >= 5
    finally:
        db.close()
