from confluent_kafka import Consumer, KafkaError
import json

config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'sample-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
consumer.subscribe(['sample'])

print("📩 Listening for messages on topic 'sample'...\n")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break

        key = msg.key().decode('utf-8') if msg.key() else None
        raw_value = msg.value().decode('utf-8') if msg.value() else ""

        # Safely try parsing as JSON; fall back to raw string if performance test payload
        try:
            payload = json.loads(raw_value)
        except json.JSONDecodeError:
            payload = f"[RAW DATA]: {raw_value}"

        print(f"Received Message:")
        print(f"   Key: {key}")
        print(f"   Payload: {payload}")
        print(f"   Partition: {msg.partition()} | Offset: {msg.offset()}\n")

except KeyboardInterrupt:
    print("\nStopping consumer...")
finally:
    consumer.close()