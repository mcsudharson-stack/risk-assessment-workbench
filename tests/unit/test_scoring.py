from src.risk_engine.scoring import calculate_risk_score


def test_medium_risk():
    result = calculate_risk_score(
        change_type="new_feature",
        geography="United States",
        customer_segment="Retail Customers",
        vendor_involved=True,
    )

    assert result["score"] == 35
    assert result["rating"] == "MEDIUM"
    assert "Moderate business change" in result["reasons"]
    assert "Third-party vendor involved" in result["reasons"]


def test_high_risk():
    result = calculate_risk_score(
        change_type="new_product",
        geography="United Kingdom",
        customer_segment="High Net Worth",
        vendor_involved=True,
    )

    assert result["score"] == 90
    assert result["rating"] == "HIGH"


def test_low_risk():
    result = calculate_risk_score(
        change_type="process_change",
        geography="United States",
        customer_segment="Retail Customers",
        vendor_involved=False,
    )

    assert result["score"] == 10
    assert result["rating"] == "LOW"