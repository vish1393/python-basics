# basics/kafka-basics/consumer-basics.py
from confluent_kafka import Consumer, KafkaError
import json
import config  # Imports configurations from config.py / .env

# 1. Initialize Consumer with manual commit configuration
consumer = Consumer(config.CONSUMER_CONFIG)
consumer.subscribe([config.TOPIC_NAME])

print(f"🎧 Listening on '{config.TOPIC_NAME}' with MANUAL COMMITS...")
print(f"Group: '{config.GROUP_ID}' | Press Ctrl+C to stop.\n")

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"❌ Consumer error: {msg.error()}")
                break

        # Process the message
        try:
            key = msg.key().decode('utf-8') if msg.key() else None
            value = json.loads(msg.value().decode('utf-8'))

            print(
                f"📩 [Partition {msg.partition()} @ Offset {msg.offset()}] "
                f"Key: {key} | Value: {value}"
            )

            # ---------------------------------------------------------------
            # MANUAL COMMIT POINT
            # Commit offset ONLY AFTER message business logic succeeds.
            # ---------------------------------------------------------------
            consumer.commit(message=msg, asynchronous=False)
            print(f"  └─ ✅ Offset {msg.offset()} manually committed.")

        except json.JSONDecodeError as decode_err:
            # Handle corrupt/malformed payload without committing or crashing
            print(f"  └─ ⚠️ Skipped malformed JSON at offset {msg.offset()}: {decode_err}")
            # Optional: commit to skip bad message, or route to DLQ

except KeyboardInterrupt:
    print("\n⚠️ Stopping consumer gracefully...")

finally:
    # Final close ensures any pending offsets or state are flushed
    consumer.close()
    print("✅ Consumer connection closed.")