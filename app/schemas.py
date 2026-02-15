from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class WebhookEventBase(BaseModel):
    event_id: str = Field(..., min_length=1)
    payload: Dict[str, Any]
    signature: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    error: Optional[str] = None


class WebhookEventOut(WebhookEventBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
