from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from triage.api.schemas import TicketRequest, TicketResponse
from triage.utils.logger import get_logger
from triage.db import crud
from triage.db.database import get_session
from triage.agents.decision import decide_status

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


@router.post("/tickets")
def submit_ticket(customer_email:str , subject:str ,body :str, session: Session = Depends(get_session)):
    ticket = crud.create_ticket(session, customer_email, subject, body)

    result = graph.invoke({"ticket_text": f"{subject} {body}"})
    top_distance = result['retrieved_context'][0]['distance'] if result['retrieved_context'] else 999

    status = decide_status(result['predicted_queue'], result['confidence'], top_distance)

    updated = crud.update_ticket_result(
        session, ticket.id, result['predicted_queue'], result['confidence'],
        result['draft_response'], result['retrieved_context'], status )

    logger.info(f"Ticket {ticket.id} -> {status}")
    return updated


@router.get("/tickets")
def get_tickes(status:str = None, session: Session = Depends(get_session)):
    return crud.list_tickets(session, status)


@router.post("/tickets/{ticket_id}/reply")
def reply_to_ticket(ticket_id: str, final_reply: str, session: Session = Depends(get_session)):
    return crud.send_reply(session, ticket_id, final_reply)


@router.get("/tickets/{ticket_id}") 
def get_single_ticket(ticket_id: str, session: Session = Depends(get_session)):
    return crud.get_ticket(session, ticket_id)

@router.get("/stats")
def get_stats(session: Session = Depends(get_session)):
    return crud.get_today_stats(session)            


