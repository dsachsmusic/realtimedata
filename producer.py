from kafka import KafkaProducer
import time
import json
import random

#create a kafka producer...which
# - Connects to Kafka
# - Handles retries, batching, buffering, etc.
# - Provides a .send() method for publishing messages
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    #note: "lambda" defines an anonymous function (one liner, more or less)
    # - v is the (only) paramater...
    #note: value_serializer here...no key_serializer
    # - not using a key...kafka is just going to assign a random partition
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

log_levels = ['INFO', 'DEBUG', 'WARN', 'ERROR']

def generate_log():
    return {
        "timestamp": time.time(),
        "level": random.choice(log_levels),
        "message": "Something happened!"
    }

#while True is like while 1 = 1 (i.e. keep running forever, until ctrl+c)
while True:
    log = generate_log()
    #send "log" to the "logs" topic
    #note: ok if not yet created, assuming auto.create.topics.enable=true
    # - to check can log into container and run:
    #   - kafka-topics --bootstrap-server localhost:9092 --list
    producer.send('logs', log)
    print(f"Sent: {log}")
    time.sleep(1)