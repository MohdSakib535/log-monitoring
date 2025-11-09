# Quick Guide: Functionality, Why, and What Works

## Services and Roles

- API (`api`): FastAPI app to ingest and list logs on port 8000. File: app/api/routes/logs.py
- Worker (`worker`): Celery worker that persists logs to Postgres. File: app/celery_app/tasks.py
- Beat (`beat`): Celery beat scheduler for periodic tasks (e.g., analytics).
- Consumer (`consumer`): Kafka consumer reading topic `logs` and enqueueing Celery tasks. File: app/kafka/consumer.py
- DB (`db`): Postgres 15 stores logs and alert-related data.
- Redis (`redis`): Celery broker and result backend.
- Kafka (`kafka`): Apache Kafka 3.7 (KRaft mode) on `kafka:9092` for async ingestion.
- Flower (`flower`): Celery monitoring UI on port 5555.

## What Works (Verified)

- API endpoints
  - POST `/logs/`: Accepts `{level, message, service_name, metadata}` and queues ingestion.
  - GET `/logs/`: Returns the latest logs from Postgres.
- Kafka path
  - Producer uses `kafka-python` to send to topic `logs`.
  - Kafka broker runs in KRaft mode with listeners `PLAINTEXT://kafka:9092` and auto-creates topics.
- Fallback path
  - If Kafka send fails, the API enqueues via Celery to maintain availability.
- Celery processing
  - Worker executes `process_log_task` and writes to the database.
- Storage model
  - Table `logs` has JSON column `metadata`. ORM attribute is `extra` mapped to DB column `metadata` (avoids SQLAlchemy reserved name).
- Monitoring
  - Flower connects to Redis and displays Celery queues/tasks at `http://localhost:5555`.

## Why These Pieces

- Kafka: Decouples ingestion from persistence and smooths traffic spikes.
- Redis + Celery: Reliable background processing for both Kafka-consumed messages and fallback.
- Fallback to Celery: Guarantees logs are accepted during Kafka outages.
- Postgres: Durable, indexed storage for querying logs and alerts.
- Flower: Operational visibility into Celery workers and tasks.
- SQLAlchemy attribute rename: Prevents conflict with declarative `metadata` while preserving DB schema.

## Data Flow

- Normal path: Client → API (`/logs/`) → Kafka topic `logs` → Consumer → Celery task → Worker → Postgres.
- Fallback path: Client → API (`/logs/`) → Celery task → Worker → Postgres.

## Key Files

- API routes: app/api/routes/logs.py
- Kafka producer: app/kafka/producer.py
- Kafka consumer: app/kafka/consumer.py
- Celery tasks: app/celery_app/tasks.py
- Persistence: app/services/log_processor.py
- Models: app/models.py
- DB setup: app/database.py
- Compose: docker-compose.yml

## Ports

- API: 8000
- Postgres: 5432
- Redis: 6379
- Kafka: 9092
- Flower: 5555

## Notes

- Use `/logs/` (trailing slash) to avoid a 307 redirect.
- Flower shows richer data if the worker runs with events enabled (`-E`).

