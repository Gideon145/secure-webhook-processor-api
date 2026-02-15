from fastapi import FastAPI

from .database import Base, engine
from .routes.webhook import router as webhook_router

app = FastAPI(title="Secure Webhook Processor API")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(webhook_router)
