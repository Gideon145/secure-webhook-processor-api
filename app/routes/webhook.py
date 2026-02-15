from typing import Any, Dict, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import WebhookEvent
from ..schemas import WebhookEventOut
from ..security import get_current_user, verify_signature
from ..services.processor import process_event

router = APIRouter()


@router.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    signature = request.headers.get("X-Signature")
    if not signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature")

    raw_body = await request.body()
    if not verify_signature(raw_body, signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    try:
        payload: Dict[str, Any] = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON")

    event_id = payload.get("event_id")
    if not event_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="event_id is required")

    existing = db.query(WebhookEvent).filter(WebhookEvent.event_id == event_id).first()
    if existing:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "already_received"})

    event = WebhookEvent(
        event_id=event_id,
        payload=payload,
        signature=signature,
        status="received",
    )
    db.add(event)
    db.commit()

    background_tasks.add_task(process_event, event_id)
    return {"status": "accepted"}


@router.get("/events", response_model=List[WebhookEventOut])
def list_events(
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    return (
        db.query(WebhookEvent)
        .order_by(WebhookEvent.created_at.desc())
        .all()
    )
