"""Here we will be defining request/response shapes"""

from pydantic import BaseModel
from typing import List, Optional

class TicketRequest(BaseModel):
    ticket_text:str


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
    escalted: Optional[bool]
        