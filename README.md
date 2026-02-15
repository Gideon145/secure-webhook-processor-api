# Secure Webhook Processor API

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

## Demo validation
The API demonstrates strong security in practice:
- HMAC-SHA256 signature validation rejects all requests with invalid signatures (401 Unauthorized)
- Valid signatures are accepted and processed asynchronously (202 Accepted)
- PostgreSQL persists events reliably
- Background tasks update event status from `received` → `processing` → `processed`

## Future improvements
- Add robust JWT issuer/audience validation
- Add retries and a real job queue
- Structured logging and tracing
- Database migrations (Alembic)
