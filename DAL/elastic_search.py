from elasticsearch import Elasticsearch
from logger.logger import Logger
logger = Logger.get_logger()


class DALElastic:

    def __init__(self, host_name, index_name, mappings = None):
        self.host = f"http://{host_name}:9200"
        self.es = Elasticsearch(self.host)
        self.index = index_name
        self.mappings = mappings


    def is_connected(self):
        connected = self.es.ping()
        logger.info(f"connected to elastic {self.host} - ready for operations")
        return connected


    def create_index(self):
        if not self.es.indices.exists(index=self.index):
            if self.mappings:
                self.es.indices.create(index=self.index, mappings=self.mappings)
                logger.info(f"create index {self.index}")
            else:
                self.es.indices.create(index=self.index)
                logger.info(f"index {self.index} already exists")


    def post_document(self, id, user):
        result =  self.es.index(index=self.index, id=id, body=user)
        print(result)