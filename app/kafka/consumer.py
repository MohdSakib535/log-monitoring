import json
import time
from kafka import KafkaConsumer

from ..config import settings
from ..celery_app.tasks import process_log_task


def run_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                settings.KAFKA_TOPIC,
                bootstrap_servers=settings.KAFKA_BROKER,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                consumer_timeout_ms=10000,
            )
            for msg in consumer:
                payload = msg.value
                process_log_task.delay(payload)
        except Exception as e:
            # Backoff and retry on connection issues
            time.sleep(5)


if __name__ == "__main__":
    run_consumer()

