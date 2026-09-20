from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.demo.seed import seed_procurement_demo_case
from app.api.cases import get_case_by_id

router = APIRouter(prefix="/demo", tags=["Demo"])

@router.post("/load")
def load_one_click_demo(db: Session = Depends(get_db)):
    """
    One-click demo initialization:
    Loads the prepared procurement evidence dataset and runs the complete investigation pipeline.
    """
    demo_case = seed_procurement_demo_case(db)
    return get_case_by_id(demo_case.id, db)
