from src.risk_engine.scoring import calculate_risk_score
from src.services.ai_service import generate_risk_assessment
from src.services.knowledge_service import retrieve_policy_context


def run_risk_assessment_workflow(change_request):
    """
    Orchestrates the AI-assisted FCRM assessment.

    Flow:
    1. Deterministic risk scoring
    2. Policy knowledge retrieval
    3. AI draft generation
    4. Human review gate

    AI is advisory only.
    Final decisions remain with humans.
    """

    workflow_steps = []

    # STEP 1: Deterministic Risk Engine
    risk_result = calculate_risk_score(
        change_type=change_request.change_type,
        geography=change_request.geography,
        customer_segment=change_request.customer_segment,
        vendor_involved=change_request.vendor_involved,
    )

    workflow_steps.append({
        "step": "risk_scoring",
        "status": "completed",
        "result": risk_result["rating"],
    })

    # STEP 2: Retrieve FCRM policy context
    policy_documents = retrieve_policy_context(change_request)

    retrieved_sources = [
        document["source"]
        for document in policy_documents
    ]

    workflow_steps.append({
        "step": "policy_retrieval",
        "status": "completed",
        "sources": retrieved_sources,
    })

    # STEP 3: Generate AI draft
    ai_draft = generate_risk_assessment(
        change_request=change_request,
        risk_result=risk_result,
    )

    workflow_steps.append({
        "step": "ai_assessment",
        "status": "completed",
    })

    # STEP 4: Human gate
    workflow_steps.append({
        "step": "human_review",
        "status": "required",
    })

    return {
        "request_id": change_request.request_id,

        "workflow_steps": workflow_steps,

        "risk_score": risk_result["score"],
        "risk_rating": risk_result["rating"],
        "risk_reasons": risk_result["reasons"],

        "retrieved_sources": retrieved_sources,

        "ai_draft": ai_draft,

        "workflow_status": "awaiting_human_review",

        "governance": {
            "human_review_required": True,
            "ai_can_approve": False,
            "ai_can_reject": False,
            "final_decision_owner": "Risk Committee",
        },
    }