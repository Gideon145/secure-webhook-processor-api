from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, JSON

from .database import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True, nullable=False)
    payload = Column(JSON, nullable=False)
    signature = Column(String, nullable=False)
    status = Column(String, nullable=False, default="received")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=True)
