# basics/kafka-basics/consumer-basics.py
from confluent_kafka import Consumer, KafkaError
import json
import config  # Imports settings from config.py / .env

# 1. Initialize Consumer using config.py
consumer = Consumer(config.CONSUMER_CONFIG)

# 2. Subscribe to the target topic
consumer.subscribe([config.TOPIC_NAME])

print(f"🎧 Listening on '{config.TOPIC_NAME}' for group '{config.GROUP_ID}'...")
print("Press Ctrl+C to stop.\n")

try:
    # 3. Infinite loop to keep polling for incoming messages
    while True:
        # poll(timeout) blocks for up to 1.0 second waiting for records
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition reached (informational only)
                continue
            else:
                print(f"❌ Consumer error: {msg.error()}")
                break

        # Decode byte payload to JSON
        key = msg.key().decode('utf-8') if msg.key() else None
        value = json.loads(msg.value().decode('utf-8'))

        print(
            f"📩 [Partition {msg.partition()} @ Offset {msg.offset()}] "
            f"Key: {key} | Value: {value}"
        )

except KeyboardInterrupt:
    print("\n⚠️ Graceful shutdown requested by user...")

finally:
    # 4. Close consumer connection and commit offsets properly
    consumer.close()
    print("✅ Consumer closed.")