from kafka import KafkaProducer
import json


class Producer:

    def __init__(self, server_uri):
        self.server_uri = server_uri
        self.producer = None


    def create_producer(self):
        if self.producer is None:
            self.producer = KafkaProducer(bootstrap_servers=[self.server_uri],
                                     value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8'))


    def flush_messages(self):
        if self.producer is not None:
            self.producer.flush()
        self.producer = None


    def publish_messages(self, topic: str, message: dict):
        if self.producer is not None:
            print("start to publish messages")
            self.producer.send(topic, message)