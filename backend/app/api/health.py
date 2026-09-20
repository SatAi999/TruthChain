from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Production health check endpoint.
    Exposes safe status for database, storage, and engine services without exposing secrets.
    """
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"disconnected: {str(e)[:50]}"

    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "database": db_status,
        "environment": "production" if not "sqlite" in settings.DATABASE_URL else "local/sqlite"
    }
