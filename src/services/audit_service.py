from sqlalchemy.orm import Session

from src.models.audit_event_db import AuditEventDB


def create_audit_event(
    db: Session,
    request_id: str,
    actor: str,
    action: str,
    from_status: str | None = None,
    to_status: str | None = None,
    details: str | None = None,
):
    event = AuditEventDB(
        request_id=request_id,
        actor=actor,
        action=action,
        from_status=from_status,
        to_status=to_status,
        details=details,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event