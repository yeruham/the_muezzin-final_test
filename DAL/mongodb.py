from pymongo import MongoClient
import gridfs
from logger.logger import Logger
logger = Logger.get_logger()


class DALMongo:

    def __init__(self, prefix, host, database, collection, user= None, password= None):
        self.prefix = prefix
        self.host = host
        self.database = database
        self.collection = collection
        self.user = user
        self.password = password
        self.URI = self.build_URI()
        self.client = None


    def build_URI(self):
        if self.user and self.password:
            URI = f"{self.prefix}://{self.user}:{self.password}@{self.host}::27017"
        else:
            URI = f"{self.prefix}://{self.host}:27017"

        return URI


    def open_connection(self):
        try:
            self.client = MongoClient(self.URI)
            self.client.admin.command("ping")
            logger.info(f"connected to mongodb {self.URI} - ready for operations")
            return True
        except Exception as e:
            self.client = None
            logger.error(f"Error during try to connect to {self.URI} : {e}")
            return False


    def insert_file(self, path, **kwargs):
        if self.client:
            db = self.client[self.database]
            grid_db = gridfs.GridFS(db, collection=self.collection)
            with open(path, "br") as f:
                grid_db.put(f, **kwargs)


    def get_file(self, id):
        if self.client:
            db = self.client[self.database]
            fs = gridfs.GridFS(db)
            for grid_out in fs.find({"id": id}):
                data = grid_out.read()
                return data



    def close_connection(self):
        if self.client:
            self.client.close()
            logger.info(f"connection to mongodb {self.URI} closed")


# example
if __name__ == "__main__":
    dal_mongo = DALMongo("mongodb", "localhost", "muezzin", "podcast")
    print(dal_mongo.open_connection())
    data = dal_mongo.get_file("download (1).wav-1979-12-31 23:00:00-2396.81 KB-")
    with open("C:\\python_data\\new_podcast\\new.wav", "bw") as f:
        f.write(data)