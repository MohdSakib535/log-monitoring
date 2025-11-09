# Log Analytics & Monitoring Platform (FastAPI)

A containerized log ingestion, analytics, and alerting platform built with FastAPI, SQLAlchemy, Celery, Redis, and Kafka. Includes a REST API for ingesting logs, computing simple analytics, and managing alert rules.

## Features
- FastAPI service for log ingestion and querying analytics
- Kafka-based ingestion pipeline (producer in API, consumer service)
- Celery worker and beat for async processing and scheduled jobs (Redis broker/result)
- PostgreSQL for persistence (logs, alert rules, events)
- Docker Compose orchestration for all services

## Quick Start

1. Copy `.env` and adjust as needed (defaults work with compose):
   - `DATABASE_URL=postgresql+psycopg2://lap:lap@db:5432/lap`
   - `REDIS_URL=redis://redis:6379/0`
   - `KAFKA_BROKER=kafka:9092`

2. Build and run:
   - `docker compose up -d --build`

3. Initialize DB (optional – app also auto-creates tables):
   - `docker compose exec api python scripts/init_db.py`

4. Open API docs:
   - http://localhost:8000/docs

5. Send sample logs:
   - `docker compose exec api python scripts/sample_logs.py`

## Services
- `api`: FastAPI app (`uvicorn app.main:app`)
- `worker`: Celery worker (`celery -A app.celery_app.celery_config.celery_app worker`)
- `beat`: Celery beat for scheduled tasks
- `consumer`: Kafka consumer that enqueues log processing tasks
- `db`: PostgreSQL 15
- `redis`: Redis 7
- `kafka`: Single-node Kafka in KRaft mode (no Zookeeper)

## Development
- Hot-reload is not enabled by default. You can mount the source volume and enable `--reload` for local dev if needed.
- Tests (basic): `pytest -q`

## AI Integration (optional, not implemented)
Yes, you can integrate AI in several places:
- Intelligent alerting: anomaly detection on error rates or latency using an ML model.
- Log summarization: LLM-generated summaries of noisy logs for quicker triage.
- Root-cause suggestions: use embeddings to search for similar incidents and proposed fixes.

For this implementation, all logic is rule/statistics based without AI.

## Environment Variables
Key variables (see `.env`):
- `DATABASE_URL`, `REDIS_URL`, `KAFKA_BROKER`, `KAFKA_TOPIC`
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- `APP_ENV` (`development`/`production`/`testing`)

## Endpoints
- `GET /health` – health check
- `POST /logs` – ingest a log (produces to Kafka; falls back to Celery when needed)
- `GET /analytics` – simple counts per level in a time window
- `GET /alerts/rules`, `POST /alerts/rules` – manage alert rules
- `GET /alerts/events` – list triggered alert events

## Notes
- This project favors simplicity. For production, add auth, rate-limiting, index tuning, monitoring, and robust Kafka topic management.
- Alembic is not included; tables auto-create at startup/scripts.
