import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.domain import Case

router = APIRouter(prefix="/cases", tags=["SSE Stream"])

@router.get("/{case_id}/stream")
async def stream_investigation_events(case_id: str, db: Session = Depends(get_db)):
    """
    Streams real-time investigation activity events to the frontend via SSE.
    """
    case_obj = db.query(Case).filter(Case.id == case_id).first()
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case not found")

    async def event_generator():
        # Stream historical steps
        steps = sorted(case_obj.steps, key=lambda s: s.step_number)
        for s in steps:
            event_data = {
                "step_number": s.step_number,
                "type": s.step_type,
                "title": s.title,
                "detail": s.detail,
                "timestamp": str(s.timestamp)
            }
            yield {
                "event": "investigation_step",
                "data": json.dumps(event_data)
            }
            await asyncio.sleep(0.3)  # Smooth presentation interval for live UI feed

        yield {
            "event": "investigation_completed",
            "data": json.dumps({"status": "COMPLETED", "verdict": case_obj.verdict})
        }

    return EventSourceResponse(event_generator())
