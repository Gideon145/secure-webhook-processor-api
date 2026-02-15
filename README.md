# Secure Webhook Processor API

A production-ready FastAPI service that validates webhook signatures, stores events in PostgreSQL, and processes them asynchronously using background tasks.

![Working Demo](screenshot.png)
*Live demonstration showing successful HMAC signature validation, webhook acceptance, and real-time processing logs*

## Overview
A production-ready FastAPI service that validates webhook signatures, stores events in PostgreSQL, and processes them asynchronously using background tasks.

## Architecture
- FastAPI for API layer
- SQLAlchemy ORM for persistence
- PostgreSQL for durable storage
- BackgroundTasks for async processing

## Security (HMAC validation)
Incoming requests must include `X-Signature` (HMAC SHA256). Requests with invalid signatures return 401.

## Idempotency handling
Duplicate `event_id` values are accepted and return 200 without reprocessing.

## Tech stack
FastAPI, PostgreSQL, SQLAlchemy, Docker

## How to run with Docker
1. Build and start services:
   ```bash
   docker-compose up --build
   ```
2. API will be available at http://localhost:8000

## Example curl request
```bash
payload='{"event_id":"evt_123","type":"invoice.paid"}'

signature=$(python - <<'PY'
import hmac, hashlib
payload=b'{"event_id":"evt_123","type":"invoice.paid"}'
secret=b'supersecret'
print(hmac.new(secret, payload, hashlib.sha256).hexdigest())
PY
)

curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Signature: ${signature}" \
  -d "${payload}"
```

## Protected dashboard
`GET /events` requires a JWT Bearer token in the `Authorization` header.

## What's in the screenshot
The screenshot demonstrates the API in action:
- **Left terminal**: Python script generating a valid HMAC-SHA256 signature for a test payload, followed by a curl command successfully posting to the `/webhook` endpoint
- **Right panel**: Docker Compose logs showing:
  - PostgreSQL database initialized and ready
  - Uvicorn server running on port 8000
  - Real-time request logs displaying multiple 401 errors (invalid signatures being rejected)
  - One successful 202 Accepted response (valid signature accepted)

This proves the HMAC validation is working correctly—rejecting bad signatures while accepting legitimate requests.

## Future improvements
- Add robust JWT issuer/audience validation
- Add retries and a real job queue
- Structured logging and tracing
- Database migrations (Alembic)
