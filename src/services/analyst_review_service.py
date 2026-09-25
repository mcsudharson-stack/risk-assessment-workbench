from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.analyst_review import AnalystReview
from src.models.change_request_db import ChangeRequestDB
from src.services.audit_service import create_audit_event


def save_analyst_review(
    db: Session,
    request: ChangeRequestDB,
    review: AnalystReview,
):
    # Validate final risk rating
    rating = review.final_risk_rating.upper()

    if rating not in ["LOW", "MEDIUM", "HIGH"]:
        raise HTTPException(
            status_code=400,
            detail="final_risk_rating must be LOW, MEDIUM, or HIGH",
        )

    # Override reason is mandatory when analyst disagrees with AI
    if review.override_ai:
        if not review.override_reason or not review.override_reason.strip():
            raise HTTPException(
                status_code=400,
                detail="override_reason is required when override_ai is true",
            )

    # Save analyst review
    request.analyst_name = review.analyst_name
    request.analyst_risk_rating = rating
    request.ai_overridden = review.override_ai
    request.override_reason = review.override_reason
    request.analyst_comments = review.comments

    db.commit()
    db.refresh(request)

    # Create audit trail
    create_audit_event(
        db=db,
        request_id=request.request_id,
        actor=review.analyst_name,
        action="ANALYST_REVIEW_COMPLETED",
        from_status=request.status,
        to_status=request.status,
        details=(
            f"Final risk rating: {rating}; "
            f"AI overridden: {review.override_ai}; "
            f"Override reason: {review.override_reason or 'Not applicable'}"
        ),
    )

    return {
        "message": "Analyst review saved successfully",
        "request_id": request.request_id,
        "analyst_name": request.analyst_name,
        "final_risk_rating": request.analyst_risk_rating,
        "ai_overridden": request.ai_overridden,
        "override_reason": request.override_reason,
        "comments": request.analyst_comments,
        "human_review_completed": True,
    }