from sqlalchemy import Column , String, Text , Float , Boolean , DateTime,Integer
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda:str(uuid.uuid4())[:8])
    customer_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)

    predicted_queue = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    draft_response = Column(Text, nullable=True)
    retrieved_context = Column(Text, nullable=True)  # stored as JSON string

    status = Column(String, default="processing")

    final_reply = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


    # In this file we have basically created a blue print of how our tickets will look like.
    # this file is used to create and update tickets in our database.
    
         
    





