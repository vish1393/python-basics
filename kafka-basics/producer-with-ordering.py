# producer_basics.py excerpt
import json
from confluent_kafka import Producer
import config

producer = Producer({
    'bootstrap.servers': config.BOOTSTRAP_SERVERS,
    'acks': 'all',
    'enable.idempotence': True,             # Prevents duplicates
    'max.in.flight.requests.per.connection': 1  # Preserves order on retry
})

# Sequential events for the SAME order
order_id = "ORDER-1001"

events = [
    {"order_id": order_id, "status": "CREATED"},
    {"order_id": order_id, "status": "PAYMENT_COMPLETED"},
    {"order_id": order_id, "status": "SHIPPED"}
]

for event in events:
    producer.produce(
        topic=config.TOPIC_NAME,
        key=order_id, # <--- KEY ENSURES SAME PARTITION!
        value=json.dumps(event)
    )
    producer.poll(0)

producer.flush()