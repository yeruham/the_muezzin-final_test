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


    def create_dal_mongodb(self, prefix, host, database, collection, user= None, password= None):
        self.mongodb = DALMongo(prefix, host, database, collection, user, password)


    def create_dal_elastic(self, host_name, index_name, mappings = None):
        self.elastic = DALElastic(host_name, index_name, mappings)


    def run_process(self):
        if isinstance(self.mongodb, DALMongo) and (isinstance(self.elastic, DALElastic) and isinstance(self.consumer, Consumer)):
            self.consumer.run_consumer_events()
            self.elastic.create_index()
            continue_run = True
            while continue_run:
                message = self._get_message()
                unique_id = self._create_unique_id(message)
                self.elastic.post_document(unique_id, message)



    def _get_message(self):
        print("waiting to message")
        messages = self.consumer.get_events()
        return next(messages)


    def _create_unique_id(self, metadata: dict):
        id = ""
        for k, v in metadata.items():
            id += str(v)
        return id


