from kafka import KafkaConsumer
import json


class Consumer:

    def __init__(self, server_uri, group, *topics):
        """ class which represents kafka-consumer - init with uri of kafka service,
            topics to listen to them, and the group to which he belongs.
            to create and run the consumer run the run_consumer_events method """
        self.server_uri = server_uri
        self.group = group
        self.topics = topics
        self.consumer_events = None


    def run_consumer_events(self):
        """ create consumer_events without time limit and start to listen to messages from kafka.
            to get the events run get_events method that return one after one in yield """
        self.consumer_events = KafkaConsumer(*self.topics,
                                     value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                     group_id=self.group,
                                     bootstrap_servers=[self.server_uri])
        print("start to consume events")



    def get_events(self):
        """ run in infinite loop with yield - all one return one message from kafka """
        if self.consumer_events is not None:
            for message in self.consumer_events:
                print(f"offset:  {message.offset}")
                print(f"topic:  {message.topic}")

                yield message.value


    def run_consumer_limited(self, timeout: int):
        """ create consumer_events with time limit and immediately start to listen to messages from kafka.
            and save the events in list. return list with messages """
        self.consumer_events = KafkaConsumer(*self.topics,
                                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                             group_id=self.group,
                                             bootstrap_servers=[self.server_uri],
                                             consumer_timeout_ms=timeout)
        events = []
        for message in self.consumer_events:
            print(f"offset:  {message.offset}")
            print(f"topic:  {message.topic}")
            events.append(message.value)
        return events