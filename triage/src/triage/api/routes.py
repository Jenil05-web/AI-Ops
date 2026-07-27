from fastapi import APIRouter
from triage.api.schemas import TicketRequest, TicketResponse
from triage.utils.logger import get_logger


router = APIRouter()
graph = None  # injected by main.py at startup

logger = get_logger(__name__)


def set_graph(g):
    global graph
    graph = g


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/process-ticket", response_model=TicketResponse)
def process_ticket(request: TicketRequest):
    logger.info(f"Processing ticket: {request.ticket_text[:50]}...")
    result = graph.invoke({"ticket_text": request.ticket_text})
    logger.info(f"Predicted queue: {result.get('predicted_queue')}, escalated: {result.get('escalated')}")
    return result
