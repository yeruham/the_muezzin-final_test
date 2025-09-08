from kafka_tools.consumer import Consumer
from DAL.mongodb import DALMongo
from DAL.elastic_search import DALElastic


class UploadManager:

    def __init__(self):
        self.mongodb = None
        self.elastic = None
        self.consumer = None


    def create_consumer(self, server_uri, group, *topics):
        self.consumer = Consumer(server_uri, group, *topics)


    def create_dal_mongodb(self, prefix, host, user= None, password= None):
        self.mongodb = DALMongo(prefix, host, user, password)


    def create_dal_elastic(self, host_name, index_name, mappings = None):
        self.elastic = DALElastic(host_name, index_name, mappings)


    def run_process(self, database, time_consumer_limited):
        if isinstance(self.mongodb, DALMongo) and (isinstance(self.elastic, DALElastic) and isinstance(self.consumer, Consumer)):
            events = self.consumer.run_consumer_limited(time_consumer_limited)
            self.elastic.create_index()
            self.mongodb.open_connection()
            for message in events:
                path = message.pop("path")
                unique_id = self._create_unique_id(message["name"], message["creation_date"], message["size"])
                self.elastic.post_document(unique_id, message)
                self.mongodb.insert_file(database ,path, id=unique_id)
            self.mongodb.close_connection()
        else:
            print(f"one of the objects is not the correct type. current self.mongodb is {type(self.mongodb)}."
                  f"current self.elastic is {type(self.elastic)}. current self.consumer is {type(self.consumer)}.")



    def _create_unique_id(self, *identifiers):
        id = ""
        for i in identifiers:
            id += f"{i}-"
        return id
