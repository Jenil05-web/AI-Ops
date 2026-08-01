from typing import TypedDict, Optional
from triage.models.classifier import load_artifacts, predict as classify_predict


class TicketState(TypedDict):
    ticket_text: str
    predicted_queue: Optional[str]
    confidence: Optional[float]
    predicted_priority: Optional[str]
    retrieved_context: Optional[list]
    draft_response: Optional[str]
    escalated: Optional[bool]


def triage_node(state: TicketState, model, vectorizer, label_encoder) -> TicketState:
    """Predict the queue for a ticket using the trained classifier."""
    predicted_queue, confidence = classify_predict(state['ticket_text'], model, vectorizer, label_encoder)
    state['predicted_queue'] = predicted_queue
    state['confidence'] = confidence
    return state


"""This triage node uses our trained classifier ML model
   classify_predict calls  trained XGBoost model , no OpenAI call happens here.
   The LLM only enters the picture later, in the Drafting Agent node."""

# basically in this file we are defining the TicketState TypedDict which represents the state of a ticket during the triage process.and then using triage agent 