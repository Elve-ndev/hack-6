from typing import List, Dict, Any, Optional
from backend.app.calculate import evaluate_income
from backend.app.rules_engine import get_income_limit_rule

def build_submission(
    household_id: str,
    annualized_income: float,
    household_size: int,
    citations: List[Dict[str, Any]],
    packet_status: str,
    review_reasons: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Assembles the final output exactly matching starter/schemas/submission.schema.json.
    """
    math_result = evaluate_income(annualized_income, household_size)
    rule = get_income_limit_rule(household_size)

    submission = {
        "household_id": household_id,
        "annualized_income": math_result["annualized_income"],
        "comparison": math_result["comparison"],
        "readiness_status": packet_status,  # must be "READY_TO_REVIEW" or "NEEDS_REVIEW"
        "citations": citations + [{
            "rule_id": rule["rule_id"],
            "source_url": rule["source_url"],
            "source_locator": rule["source_locator"],
        }],
    }

    if review_reasons:
        submission["review_reasons"] = review_reasons

    return submission
