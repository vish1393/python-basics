# producer_basics.py
from confluent_kafka import Producer
import json
import time
import config  # Imports configurations from config.py / .env

# 1. Initialize Producer using loaded configuration
producer = Producer(config.PRODUCER_CONFIG)

# 2. Delivery report callback to confirm message arrival
def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(
            f"✅ Topic: '{msg.topic()}' | "
            f"Partition: {msg.partition()} | "
            f"Offset: {msg.offset()} | "
            f"Key: {msg.key().decode('utf-8') if msg.key() else None}"
        )

print(f"🚀 Producing test events to topic '{config.TOPIC_NAME}'...\n")

# 3. Produce sample messages
try:
    for i in range(1, 6):
        payload = {
            "order_id": 1000 + i,
            "status": "CREATED",
            "amount": round(15.50 * i, 2)
        }
        
        # Using partition keys to demonstrate key-based hashing
        key = f"customer-{i % 2}"

        producer.produce(
            topic=config.TOPIC_NAME,
            key=key,
            value=json.dumps(payload),
            callback=delivery_report
        )
        
        # Poll events to handle delivery callbacks asynchronously
        producer.poll(0)
        time.sleep(0.2)

except Exception as e:
    print(f"Error producing message: {e}")

finally:
    # 4. Flush forces buffered messages to be sent before exiting
    print("\nFlushing remaining messages...")
    producer.flush()
    print("Done!")