from kafka import KafkaConsumer
import json


class Consumer:

    def __init__(self, server_uri, *topics):
        self.server_uri = server_uri
        self.consumer_events = None
        self.topics = topics


    def run_consumer_events(self):
        self.consumer_events = KafkaConsumer(*self.topics,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                 group_id='text-group',
                                 bootstrap_servers=[self.server_uri])
        print("start to consume events")


    def get_events(self):
        if self.consumer_events is not None:
            for message in self.consumer_events:
                print(f"offset:  {message.offset}")
                print(f"topic:  {message.topic}")

                yield message