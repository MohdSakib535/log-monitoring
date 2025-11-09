import json
from threading import Lock
from typing import Optional

from kafka import KafkaProducer as _KafkaProducer

from ..config import settings

_producer: Optional[_KafkaProducer] = None
_lock = Lock()


def _init_producer() -> _KafkaProducer:
    return _KafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        api_version_auto_timeout_ms=30000,
    )


def get_producer() -> _KafkaProducer:
    global _producer
    if _producer is None:
        with _lock:
            if _producer is None:
                _producer = _init_producer()
    return _producer


class Producer:
    def __init__(self):
        self._p = get_producer()

    def produce(self, payload: dict) -> None:
        self._p.send(settings.KAFKA_TOPIC, payload)
        self._p.flush(1)


def produce(payload: dict) -> None:
    Producer().produce(payload)
