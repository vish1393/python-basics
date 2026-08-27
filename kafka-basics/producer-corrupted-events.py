# produce_corrupted_events.py
import json
from confluent_kafka import Producer
import config

# Initialize producer using settings from config.py / .env
producer = Producer(config.PRODUCER_CONFIG)

def delivery_report(err, msg):
    if err:
        print(f"❌ Failed to deliver message: {err}")
    else:
        print(f"📦 Sent -> Partition {msg.partition()} @ Offset {msg.offset()} | Key: {msg.key().decode('utf-8') if msg.key() else None}")

print(f"🚀 Injecting test events into '{config.TOPIC_NAME}'...\n")

# Test Cases: Combination of valid, missing-field, and unparseable data
test_payloads = [
    # 1. Valid Message
    {"key": "ORD-101", "value": json.dumps({"order_id": 101, "amount": 49.99, "status": "CREATED"})},

    # 2. Invalid Message: Missing mandatory field 'amount' (triggers ValueError in consumer)
    {"key": "ORD-102", "value": json.dumps({"order_id": 102, "status": "CREATED"})},

    # 3. Corrupted Message: Malformed JSON syntax (triggers JSONDecodeError in consumer)
    {"key": "ORD-103", "value": "{ 'order_id': 103, INVALID_JSON_PAYLOAD }"},

    # 4. Valid Message
    {"key": "ORD-104", "value": json.dumps({"order_id": 104, "amount": 120.50, "status": "CREATED"})},

    # 5. Invalid Message: Null/empty string payload
    {"key": "ORD-105", "value": "NOT_EVEN_JSON"}
]

for item in test_payloads:
    producer.produce(
        topic=config.TOPIC_NAME,
        key=item["key"],
        value=item["value"],
        callback=delivery_report
    )
    # Flush events out immediately to preserve injection sequence
    producer.poll(0)

producer.flush()
print("\n✅ All test events successfully published.")