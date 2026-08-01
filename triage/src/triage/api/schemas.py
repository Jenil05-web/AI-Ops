"""Here we will be defining request/response shapes"""

from pydantic import BaseModel
from typing import List, Optional

class TicketRequest(BaseModel):
    ticket_text:str


class SubmitTicketRequest(BaseModel):
    customer_email: str
    subject: str
    body: str


class RetrievedItem(BaseModel):
    subject: str
    body: str
    answer : str
    distance : float

class TicketResponse(BaseModel):

    ticket_text :str
    predicted_queue: Optional[str]
    retrieved_context : Optional[List[RetrievedItem]]
    draft_response: Optional[str]
    escalated: Optional[bool]
        