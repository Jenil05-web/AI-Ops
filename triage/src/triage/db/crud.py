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
    ticket.retrieved_context = retrieved_context
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