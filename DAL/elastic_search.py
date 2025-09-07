from elasticsearch import Elasticsearch


class DALElastic:

    def __init__(self, host_name, index_name, mappings = None):
        host = f"http://{host_name}:9200"
        self.es = Elasticsearch(host)
        self.index = index_name
        self.mappings = mappings


    def is_connected(self):
        connected = self.es.ping()
        return connected


    def create_index(self):
        if not self.es.indices.exists(index=self.index):
            if self.mappings:
                self.es.indices.create(index=self.index, mappings=self.mappings)
            else:
                self.es.indices.create(index=self.index)


    def post_document(self, id, user):
        result =  self.es.index(index=self.index, id=id, body=user)
        print(result)