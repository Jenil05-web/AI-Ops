HIGH_RISK_QUEUES = {"Billing and Payments", "Service Outages and Maintenance", "Human Resources"}

CONFIDENCE_AUTO_RESOLVE_THRESHOLD = 0.35
DISTANCE_GOOD_MATCH_THRESHOLD = 1.0

def decide_status(predicted_queue: str, confidence: float, top_context_distance: float) -> str:
    """
    Decide whether a ticket can be auto-resolved, needs human review,
    or should be escalated immediately.
    """
    if predicted_queue in HIGH_RISK_QUEUES:
        return "needs_review"  # never auto-send on money/outage/HR topics

    if confidence < 0.3 or top_context_distance > 1.2:
        return "escalated"  # low trust in routing AND weak grounding — don't even draft confidently

    if confidence >= CONFIDENCE_AUTO_RESOLVE_THRESHOLD and top_context_distance <= DISTANCE_GOOD_MATCH_THRESHOLD:
        return "auto_resolved"

    return "needs_review"

