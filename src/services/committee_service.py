from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.change_request_db import ChangeRequestDB
from src.models.committee_decision import CommitteeDecision
from src.services.audit_service import create_audit_event


def save_committee_decision(
    db: Session,
    request: ChangeRequestDB,
    committee_decision: CommitteeDecision,
):
    if request.status != "committee_review":
        raise HTTPException(
            status_code=409,
            detail=(
                "Committee decision is only allowed when "
                "status is 'committee_review'"
            ),
        )

    old_status = request.status

    request.decision = committee_decision.decision

    if committee_decision.decision in [
        "approved",
        "rejected",
    ]:
        request.status = "decided"

    elif committee_decision.decision == "changes_requested":
        request.status = "under_review"

    db.commit()
    db.refresh(request)

    create_audit_event(
        db=db,
        request_id=request.request_id,
        actor=committee_decision.committee_member,
        action="COMMITTEE_DECISION",
        from_status=old_status,
        to_status=request.status,
        details=(
            f"Decision: {committee_decision.decision}; "
            f"Reason: {committee_decision.reason}"
        ),
    )

    return {
        "message": "Committee decision recorded successfully",
        "request_id": request.request_id,
        "decision": request.decision,
        "status": request.status,
        "decided_by": committee_decision.committee_member,
        "reason": committee_decision.reason,
    }