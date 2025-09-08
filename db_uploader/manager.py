from kafka_tools.consumer import Consumer
from DAL.mongodb import DALMongo
from DAL.elastic_search import DALElastic
from logger.logger import Logger
logger = Logger.get_logger()


class UploadManager:

    def __init__(self):
        """ class for management upload files to mongodb and their metadata to elastic.
            consume the metadata from kafka.
                for the process you need first to init three methods:
                 create_consumer, create_dal_mongodb, create_dal_elastic. """
        self.mongodb = None
        self.elastic = None
        self.consumer = None


    def create_consumer(self, server_uri, group, *topics):
        self.consumer = Consumer(server_uri, group, *topics)


    def create_dal_mongodb(self, prefix, host, database, collection, user= None, password= None):
        self.mongodb = DALMongo(prefix, host, database, collection, user, password)


    def create_dal_elastic(self, host_name, index_name, mappings = None):
        self.elastic = DALElastic(host_name, index_name, mappings)


    def run_process(self, database, time_consumer_limited):
        """ run the process - a: consumer messages of metadata from kafka.
         b: connected to elastic and sending to him the metadata.
         c: connected to mongodb and sending to him the file itself"""

        if isinstance(self.mongodb, DALMongo) and (isinstance(self.elastic, DALElastic) and isinstance(self.consumer, Consumer)):
            logger.info("start the process of upload files and their metadata to elastic and mongodb")

            # consume events and open connections
            events = self.consumer.run_consumer_limited(time_consumer_limited)
            connected_to_elastic = self.elastic.is_connected()
            connected_to_mongo_db = self.mongodb.open_connection()

            if connected_to_elastic:
                self.elastic.create_index()

            # loop on all received message - create unique id, send his to elastic, send the file by the path to mongodb
            for message in events:
                path = message.pop("path")
                unique_id = self._create_unique_id(message["name"], message["creation_date"], message["size"])
                if connected_to_elastic:
                    self.elastic.post_document(unique_id, message)
                if connected_to_mongo_db:
                    self.mongodb.insert_file(path, id=unique_id)

            self.mongodb.close_connection()
            logger.info(f"finish the process of upload files and their metadata. "
                        f"{len(events)} were accepted from kafka and sends to elastic and mongodb.")
        else:
            logger.error(f"one of the objects is not the correct type. current self.mongodb is {type(self.mongodb)}."
                  f"current self.elastic is {type(self.elastic)}. current self.consumer is {type(self.consumer)}.")



    def _create_unique_id(self, *identifiers):
        id = ""
        for i in identifiers:
            id += f"{i}-"
        return id
