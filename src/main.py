from fastapi import FastAPI

from src.api.change_requests import router as change_request_router
from src.config.database import Base, engine
from src.models.audit_event_db import AuditEventDB
from src.models.change_request_db import ChangeRequestDB


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Risk Assessment Workbench",
    description="AI-assisted financial crime risk assessment platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "application": "Risk Assessment Workbench",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(change_request_router)