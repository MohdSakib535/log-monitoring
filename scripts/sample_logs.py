import os
import random
import time
import requests


URL = os.environ.get("API_URL", "http://localhost:8000/logs/")

LEVELS = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
SERVICES = ["web", "worker", "auth", "billing", "search"]


def main(n: int = 20, delay: float = 0.1):
    for i in range(n):
        payload = {
            "level": random.choice(LEVELS),
            "message": f"sample log {i}",
            "service_name": random.choice(SERVICES),
            "metadata": {"index": i},
        }
        r = requests.post(URL, json=payload, timeout=5)
        print(i, r.status_code, r.json())
        time.sleep(delay)


if __name__ == "__main__":
    main()

