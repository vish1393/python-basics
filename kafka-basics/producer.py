from confluent_kafka import Producer
import json

producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Sending 9 messages with different keys
for i in range(1, 10):
    key = f"user-{i}"
    payload = json.dumps({"id": i, "data": f"Message {i}"})
    
    producer.produce(
        topic='sample',
        key=key,
        value=payload,
        callback=lambda err, msg: print(f"Sent to Partition {msg.partition()} @ Offset {msg.offset()}")
    )

producer.flush()