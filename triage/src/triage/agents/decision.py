import logging
_log = logging.getLogger(__name__)

# Queues that always need a human — no AI draft ever sent unsupervised
ALWAYS_HUMAN_QUEUES = {"Service Outages and Maintenance", "Human Resources"}

# Queues where we need higher confidence before auto-resolving
HIGH_CAUTION_QUEUES = {"Billing and Payments"}

CONFIDENCE_AUTO_RESOLVE_THRESHOLD = 0.22   # covers ~60-70% of real queries
CONFIDENCE_BILLING_THRESHOLD      = 0.50   # billing still needs a higher bar
DISTANCE_GOOD_MATCH_THRESHOLD     = 1.15   # L2 distance — good RAG match

def decide_status(predicted_queue: str, confidence: float, top_context_distance: float) -> str:
    """
    Decide whether a ticket can be auto-resolved, needs human review,
    or should be escalated immediately.
    """
    # HR and Outages: always send to human, no exceptions
    if predicted_queue in ALWAYS_HUMAN_QUEUES:
        return "needs_review"

    # Billing: escalate all money-related tickets immediately
    if predicted_queue in HIGH_CAUTION_QUEUES:
        return "escalated"

    # All other queues: escalate only on very low confidence or very poor RAG match
    if confidence < 0.18 or top_context_distance > 1.5:
        status = "escalated"
    elif confidence >= CONFIDENCE_AUTO_RESOLVE_THRESHOLD and top_context_distance <= DISTANCE_GOOD_MATCH_THRESHOLD:
        status = "auto_resolved"
    else:
        status = "needs_review"

    _log.info(
        f"decide_status | queue={predicted_queue!r} conf={confidence:.3f} "
        f"dist={top_context_distance:.3f} thresh=({CONFIDENCE_AUTO_RESOLVE_THRESHOLD}/{DISTANCE_GOOD_MATCH_THRESHOLD}) "
        f"-> {status}"
    )
    return status
