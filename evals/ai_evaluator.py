REQUIRED_RISK_AREAS = [
    "money laundering",
    "sanctions",
    "fraud",
    "customer",
    "geographic",
    "vendor",
]


def evaluate_ai_assessment(ai_text: str):
    text = ai_text.lower()

    risk_area_results = {}

    for risk_area in REQUIRED_RISK_AREAS:
        risk_area_results[risk_area] = risk_area in text

    covered_areas = sum(risk_area_results.values())

    coverage_score = round(
        covered_areas / len(REQUIRED_RISK_AREAS),
        2,
    )

    human_control_present = any(
        phrase in text
        for phrase in [
            "human",
            "analyst",
            "risk committee",
            "final decision",
        ]
    )

    missing_information_present = any(
        phrase in text
        for phrase in [
            "missing information",
            "additional information",
            "information required",
            "not provided",
        ]
    )

    return {
        "risk_area_coverage": risk_area_results,
        "coverage_score": coverage_score,
        "human_control_present": human_control_present,
        "missing_information_present": missing_information_present,
        "passed": (
            coverage_score >= 0.80
            and human_control_present
        ),
    }