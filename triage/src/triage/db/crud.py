import json
from datetime import datetime
from triage.db.models import Ticket
from triage.db.database import get_session

def create_ticket(session, customer_email:str, subject:str,body:str)->Ticket:
    ticket = Ticket(customer_email=customer_email, subject=subject, body = body)
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket


def update_ticket_result(session, ticket_id: str, predicted_queue: str, confidence: float,draft_response: str, retrieved_context: list, status: str) -> Ticket:
    ticket = session.query(Ticket).filter(Ticket.id==ticket_id).first()
    ticket.predicted_queue = predicted_queue
    ticket.confidence = confidence
    ticket.draft_response = draft_response
    ticket.retrieved_context = json.dumps(retrieved_context) if retrieved_context is not None else None
    ticket.status = status
    if status == "auto_resolved":
        ticket.final_reply = draft_response
        ticket.resolved_at = datetime.utcnow()
    session.commit()
    session.refresh(ticket)
    return ticket   

def get_ticket(session, ticket_id: str) -> Ticket:
    return session.query(Ticket).filter(Ticket.id == ticket_id).first()


def list_tickets(session, status: str = None):
    query = session.query(Ticket)
    if status:
        query = query.filter(Ticket.status == status)
    return query.order_by(Ticket.created_at.desc()).all()


def send_reply(session, ticket_id: str, final_reply: str) -> Ticket:
    ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
    ticket.final_reply = final_reply
    ticket.status = "resolved"
    ticket.resolved_at = datetime.utcnow()
    session.commit()
    session.refresh(ticket)
    return ticket    
    
# In this file basically the functions are used to create, update and delete the tickets in our database.

def get_today_stats(session):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond = 0)    
    tickets_today = session.query(Ticket).filter(Ticket.created_at >= today_start).all()
    
    total = len(tickets_today)
    auto_resolved = sum(1 for t in tickets_today if t.status == "auto_resolved")
    needs_review = sum(1 for t in tickets_today if t.status == "needs_review")
    escalated = sum(1 for t in tickets_today if t.status == "escalated")
    resolved = sum(1 for t in tickets_today if t.status == "resolved")

    return {
        "total": total,
        "auto_resolved": auto_resolved,
        "needs_review": needs_review,
        "escalated": escalated,
        "resolved": resolved,
        "automation_rate": round(auto_resolved / total * 100, 1) if total else 0
    }