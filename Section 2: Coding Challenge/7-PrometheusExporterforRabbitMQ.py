from prometheus_client import start_http_server, Gauge
import requests
import os
import time

# Environment Variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

# Metrics
messages = Gauge('rabbitmq_individual_queue_messages', 'Total messages', ['host', 'vhost', 'name'])
messages_ready = Gauge('rabbitmq_individual_queue_messages_ready', 'Messages ready', ['host', 'vhost', 'name'])
messages_unack = Gauge('rabbitmq_individual_queue_messages_unacknowledged', 'Messages unacknowledged', ['host', 'vhost', 'name'])

def fetch_queue_metrics():
    url = f"http://{RABBITMQ_HOST}:15672/api/queues"
    response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
    if response.status_code == 200:
        data = response.json()
        for queue in data:
            vhost = queue['vhost']
            name = queue['name']
            host = RABBITMQ_HOST
            messages.labels(host, vhost, name).set(queue['messages'])
            messages_ready.labels(host, vhost, name).set(queue['messages_ready'])
            messages_unack.labels(host, vhost, name).set(queue['messages_unacknowledged'])

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        fetch_queue_metrics()
        time.sleep(30)
