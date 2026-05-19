from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "outbreak-events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("WHO Kafka Consumer Running...")

for msg in consumer:
    event = msg.value
    print("Received outbreak event:", event)
