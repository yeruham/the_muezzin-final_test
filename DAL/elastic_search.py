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


    def post_document(self, id, document):
        result =  self.es.index(index=self.index, id=id, body=document)
        print(result)


    def update_document(self, id, updated_details):
        result = self.es.update(index=self.index, id=str(id), doc=updated_details)
        print(result)


    def get_documents(self):
        query = {"size": 10000,
                "query": {
                    "match_all": {}
        }}
        response = self.es.search(index=self.index, body=query)
        data = []
        hits = response["hits"]["hits"]
        for doc in hits:
            info = doc["_source"]
            info.update({"_id": doc["_id"]})
            data.append(info)
        return data



    def get_only_id_of_all_documents(self):
        query = {"size": 10000,
                "query": {
                    "match_all": {}
                },
                "_source": "false",
                }
        response = self.es.search(index=self.index, body=query)
        print(response)
        hits = response["hits"]["hits"]
        data = []
        for doc in hits:
            data.append(doc["_id"])
        return data


if __name__ == "__main__":
    dal_elastic = DALElastic("localhost", "muezzin")
    if dal_elastic.is_connected():
        ids = dal_elastic.get_only_id_of_all_documents()
        print(ids)
