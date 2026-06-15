from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.db.session import engine

app = FastAPI(title="Network Optimizer", version="1.0.0")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
    }

@app.get("/db-health")
def database_health_check():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar_one()

        return {
            "database": "ok",
            "result": result,
        }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(exc)}",
        ) from exc