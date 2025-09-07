from kafka import KafkaProducer
import json


class Producer:

    def __init__(self, server_uri):
        """ class which represents kafka-producer - init with uri of kafka service
            to create the producer run the create_producer method """
        self.server_uri = server_uri
        self.producer = None


    def create_producer(self):
        """ create producer on the self.producer variable """
        if self.producer is None:
            self.producer = KafkaProducer(bootstrap_servers=[self.server_uri],
                                     value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8'))


    def flush_messages(self):
        """ flush messages that were sent """
        if self.producer is not None:
            self.producer.flush()


    def publish_messages(self, topic: str, message: dict):
        """ publish any message the chosen topic - receives name of topic and dict with message """
        if self.producer is not None:
            print("start to publish messages")
            self.producer.send(topic, message)


    def close_producer(self):
        """ close the producer - the self.producer becomes to be None """
        if self.producer is not None:
            self.producer.close(timeout=10)
        self.producer = None