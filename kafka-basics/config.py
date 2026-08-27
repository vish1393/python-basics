# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME", "order-events")
DLQ_TOPIC_NAME = os.getenv("KAFKA_DLQ_TOPIC_NAME", "order-events-dlq")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "order-processing-group")

PRODUCER_CONFIG = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'acks': 'all',
    'enable.idempotence': True
}

CONSUMER_CONFIG = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'auto.offset.reset': os.getenv("KAFKA_CONSUMER_AUTO_OFFSET_RESET", "earliest"),
    'enable.auto.commit': False  # Manual commit required for DLQ pattern
}