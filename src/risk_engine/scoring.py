def calculate_risk_score(
    change_type: str,
    geography: str,
    customer_segment: str,
    vendor_involved: bool,
):
    score = 0
    reasons = []

    # Change type
    if change_type in ["new_product", "new_geography"]:
        score += 30
        reasons.append("Major business change")

    elif change_type in ["new_feature", "new_vendor"]:
        score += 20
        reasons.append("Moderate business change")

    else:
        score += 10
        reasons.append("Lower-impact process change")

    # Geography
    if geography.lower() not in ["united states", "canada"]:
        score += 25
        reasons.append("Additional geographic risk")

    # Customer segment
    if customer_segment.lower() in [
        "high net worth",
        "corporate customers",
    ]:
        score += 20
        reasons.append("Higher-risk customer segment")

    # Vendor
    if vendor_involved:
        score += 15
        reasons.append("Third-party vendor involved")

    # Final rating
    if score >= 60:
        rating = "HIGH"
    elif score >= 30:
        rating = "MEDIUM"
    else:
        rating = "LOW"

    return {
        "score": score,
        "rating": rating,
        "reasons": reasons,
    }