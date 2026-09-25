from evals.ai_evaluator import evaluate_ai_assessment


def test_good_ai_assessment():
    ai_text = """
    Money laundering risk exists because funds can move
    internationally.

    Sanctions exposure should be reviewed for destination
    countries.

    Fraud risk includes unauthorized transactions.

    Customer risk should consider the affected customer
    population.

    Geographic risk exists because international payments
    may involve multiple jurisdictions.

    Vendor risk exists because a third-party provider is
    involved.

    Missing information includes destination countries and
    transaction monitoring controls.

    The FCRM analyst must review the assessment and the
    Risk Committee retains the final decision.
    """

    result = evaluate_ai_assessment(ai_text)

    assert result["coverage_score"] == 1.0
    assert result["human_control_present"] is True
    assert result["missing_information_present"] is True
    assert result["passed"] is True


def test_weak_ai_assessment():
    ai_text = """
    This change has some financial crime risk.
    """

    result = evaluate_ai_assessment(ai_text)

    assert result["coverage_score"] < 0.80
    assert result["passed"] is False