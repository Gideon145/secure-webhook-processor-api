import asyncio
from datetime import datetime

from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import WebhookEvent


async def process_event(event_id: str) -> None:
    db: Session = SessionLocal()
    try:
        event = db.query(WebhookEvent).filter(WebhookEvent.event_id == event_id).first()
        if not event:
            return

        event.status = "processing"
        db.commit()

        await asyncio.sleep(2)

        event.status = "processed"
        event.processed_at = datetime.utcnow()
        db.commit()
    except Exception as exc:
        db.rollback()
        event = db.query(WebhookEvent).filter(WebhookEvent.event_id == event_id).first()
        if event:
            event.status = "failed"
            event.error = str(exc)
            db.commit()
    finally:
        db.close()
