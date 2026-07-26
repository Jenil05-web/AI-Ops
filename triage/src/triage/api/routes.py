from fastapi import APIRouter
from triage.api.schemas import TicketRequest, TicketResponse

router = APIRouter()
graph = None  # injected by main.py at startup


def set_graph(g):
    global graph
    graph = g


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/process-ticket", response_model=TicketResponse)
def process_ticket(request: TicketRequest):
    result = graph.invoke({"ticket_text": request.ticket_text})
    return result
