# basics/kafka-basics/consumer_dlq.py
from confluent_kafka import Consumer, Producer, KafkaError
import json
import time
import config  # Imports settings from config.py / .env

# 1. Initialize Consumer & DLQ Producer
consumer = Consumer(config.CONSUMER_CONFIG)
dlq_producer = Producer(config.PRODUCER_CONFIG)

# 2. Subscribe to the main topic
consumer.subscribe([config.TOPIC_NAME])

print(f"🎧 Listening on topic: '{config.TOPIC_NAME}'...")
print(f"🚨 Target DLQ Topic:  '{config.DLQ_TOPIC_NAME}'")
print(f"👥 Consumer Group:    '{config.GROUP_ID}'")
print("Press Ctrl+C to stop.\n")

def dlq_delivery_report(err, msg):
    """Callback to confirm DLQ write success or failure."""
    if err:
        print(f"  ❌ Failed to write message to DLQ: {err}")
    else:
        print(
            f"  └─ 🚨 Confirmed written to DLQ '{msg.topic()}' "
            f"[Partition {msg.partition()} @ Offset {msg.offset()}]"
        )

def send_to_dlq(original_msg, error_reason):
    """Publishes failed message payload + error metadata to the DLQ topic."""
    dlq_payload = {
        "original_topic": original_msg.topic(),
        "original_partition": original_msg.partition(),
        "original_offset": original_msg.offset(),
        "error_type": type(error_reason).__name__,
        "error_details": str(error_reason),
        "failed_at": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
        "raw_value": original_msg.value().decode('utf-8', errors='replace') if original_msg.value() else None
    }

    try:
        # Publish to DLQ
        dlq_producer.produce(
            topic=config.DLQ_TOPIC_NAME,
            key=original_msg.key(),  # Retain original partitioning key
            value=json.dumps(dlq_payload),
            callback=dlq_delivery_report
        )
        # Force immediate network delivery to prevent buffered message loss
        dlq_producer.flush(timeout=5.0)

    except Exception as e:
        print(f"  ❌ CRITICAL: Exception during DLQ dispatch: {e}")

# 3. Processing Loop
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

        # Attempt to process incoming record
        try:
            raw_data = msg.value().decode('utf-8')
            payload = json.loads(raw_data)

            # Business validation rule check
            if "amount" not in payload:
                raise ValueError("Missing mandatory business field: 'amount'")

            key = msg.key().decode('utf-8') if msg.key() else None
            print(
                f"✅ Processed [Partition {msg.partition()} @ Offset {msg.offset()}] "
                f"Key: {key} | Value: {payload}"
            )

            # Commit offset after successful processing
            consumer.commit(message=msg, asynchronous=False)

        except Exception as err:
            # Handle failure: route bad payload to DLQ & advance original offset
            print(f"\n⚠️ Processing Failed at Offset {msg.offset()}: {err}")
            send_to_dlq(msg, error_reason=err)
            
            # Commit original offset so consumer doesn't block on bad record
            consumer.commit(message=msg, asynchronous=False)

except KeyboardInterrupt:
    print("\n⚠️ Stopping consumer gracefully...")

finally:
    # Ensure remaining DLQ writes are sent and consumer offsets are saved
    dlq_producer.flush(timeout=5.0)
    consumer.close()
    print("✅ Consumer connection closed.")