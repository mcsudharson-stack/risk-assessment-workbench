from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.change_request import ChangeRequest
from src.models.change_request_db import ChangeRequestDB
from src.models.audit_event_db import AuditEventDB
from src.risk_engine.scoring import calculate_risk_score
from src.services.ai_service import generate_risk_assessment
from src.services.audit_service import create_audit_event
from src.workflows.risk_assessment_workflow import run_risk_assessment_workflow
from src.services.analyst_review_service import save_analyst_review
from src.models.analyst_review import AnalystReview
from src.models.committee_decision import CommitteeDecision
from src.services.committee_service import save_committee_decision


router = APIRouter(
    prefix="/api/change-requests",
    tags=["Change Requests"],
)


# ---------------------------------------------------------
# 1. CREATE CHANGE REQUEST
# ---------------------------------------------------------

@router.post("/")
def create_change_request(
    request: ChangeRequest,
    db: Session = Depends(get_db),
):
    db_request = ChangeRequestDB(
        request_id=request.request_id,
        name=request.name,
        description=request.description,
        change_type=request.change_type.value,
        business_unit=request.business_unit,
        geography=request.geography,
        customer_segment=request.customer_segment,
        vendor_involved=request.vendor_involved,
        submitted_by=request.submitted_by,
        status=request.status.value,
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return {
        "message": "Change request saved successfully",
        "request_id": db_request.request_id,
    }


# ---------------------------------------------------------
# 2. GET ALL CHANGE REQUESTS
# ---------------------------------------------------------

@router.get("/")
def get_change_requests(
    db: Session = Depends(get_db),
):
    requests = db.query(ChangeRequestDB).all()

    return requests


# ---------------------------------------------------------
# 3. GET ONE CHANGE REQUEST
# ---------------------------------------------------------

@router.get("/{request_id}")
def get_change_request(
    request_id: str,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    return request


# ---------------------------------------------------------
# 4. START FCRM REVIEW
# submitted -> under_review
# ---------------------------------------------------------

@router.patch("/{request_id}/start-review")
def start_review(
    request_id: str,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    if request.status != "submitted":
        raise HTTPException(
            status_code=409,
            detail=f"Cannot start review from status '{request.status}'",
        )

    request.status = "under_review"

    db.commit()
    db.refresh(request)

    return {
        "message": "Change request is now under review",
        "request_id": request.request_id,
        "status": request.status,
    }


# ---------------------------------------------------------
# 5. SEND TO RISK COMMITTEE
# under_review -> committee_review
# ---------------------------------------------------------

@router.patch("/{request_id}/send-to-committee")
def send_to_committee(
    request_id: str,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    if request.status != "under_review":
        raise HTTPException(
            status_code=409,
            detail=f"Cannot send to committee from status '{request.status}'",
        )

    request.status = "committee_review"

    db.commit()
    db.refresh(request)

    return {
        "message": "Change request sent to committee",
        "request_id": request.request_id,
        "status": request.status,
    }


# ---------------------------------------------------------
# 6. COMMITTEE APPROVAL
# committee_review -> decided
# ---------------------------------------------------------

@router.patch("/{request_id}/approve")
def approve_change_request(
    request_id: str,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    if request.status != "committee_review":
        raise HTTPException(
            status_code=409,
            detail=f"Cannot approve from status '{request.status}'",
        )

    request.decision = "approved"
    request.status = "decided"

    db.commit()
    db.refresh(request)

    return {
        "message": "Change request approved by committee",
        "request_id": request.request_id,
        "status": request.status,
        "decision": request.decision,
    }


# ---------------------------------------------------------
# 7. DETERMINISTIC RISK SCORE
# ---------------------------------------------------------

@router.get("/{request_id}/risk-score")
def get_risk_score(
    request_id: str,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    result = calculate_risk_score(
        change_type=request.change_type,
        geography=request.geography,
        customer_segment=request.customer_segment,
        vendor_involved=request.vendor_involved,
    )

    return {
        "request_id": request.request_id,
        "risk_score": result["score"],
        "risk_rating": result["rating"],
        "reasons": result["reasons"],
    }


# ---------------------------------------------------------
# 8. AI DRAFT ASSESSMENT
# ---------------------------------------------------------

@router.get("/{request_id}/ai-assessment")
def get_ai_assessment(
    request_id: str,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    risk_result = calculate_risk_score(
        change_type=request.change_type,
        geography=request.geography,
        customer_segment=request.customer_segment,
        vendor_involved=request.vendor_involved,
    )

    ai_draft = generate_risk_assessment(
        change_request=request,
        risk_result=risk_result,
    )

    return {
        "request_id": request.request_id,
        "risk_score": risk_result["score"],
        "risk_rating": risk_result["rating"],
        "ai_draft_assessment": ai_draft,
        "human_review_required": True,
    }


# ---------------------------------------------------------
# 9. RUN COMPLETE AI ASSESSMENT WORKFLOW
# ---------------------------------------------------------

@router.post("/{request_id}/run-assessment")
def run_assessment(
    request_id: str,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    result = run_risk_assessment_workflow(request)

    create_audit_event(
        db=db,
        request_id=request.request_id,
        actor="AI_WORKFLOW",
        action="AI_ASSESSMENT_GENERATED",
        from_status=request.status,
        to_status=request.status,
       details=(
    f"Risk rating: {result['risk_rating']}; "
    f"Risk score: {result['risk_score']}; "
    f"Human review required: "
    f"{result['governance']['human_review_required']}"
),
    )

    return result


# ---------------------------------------------------------
# 10. GET AUDIT HISTORY
# ---------------------------------------------------------

@router.get("/{request_id}/audit-history")
def get_audit_history(
    request_id: str,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    events = (
        db.query(AuditEventDB)
        .filter(AuditEventDB.request_id == request_id)
        .order_by(AuditEventDB.event_id.asc())
        .all()
    )

    return {
        "request_id": request_id,
        "audit_events": events,
    }
# ---------------------------------------------------------
# 11. FCRM ANALYST HUMAN REVIEW
# ---------------------------------------------------------

@router.post("/{request_id}/analyst-review")
def submit_analyst_review(
    request_id: str,
    review: AnalystReview,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    result = save_analyst_review(
        db=db,
        request=request,
        review=review,
    )

    return result
# ---------------------------------------------------------
# 12. RISK COMMITTEE FINAL DECISION
# ---------------------------------------------------------

@router.post("/{request_id}/committee-decision")
def submit_committee_decision(
    request_id: str,
    committee_decision: CommitteeDecision,
    db: Session = Depends(get_db),
):
    request = (
        db.query(ChangeRequestDB)
        .filter(ChangeRequestDB.request_id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    result = save_committee_decision(
        db=db,
        request=request,
        committee_decision=committee_decision,
    )

    return result