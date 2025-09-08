from pymongo import MongoClient
import gridfs
from logger.logger import Logger
logger = Logger.get_logger()


class DALMongo:

    def __init__(self, prefix, host, user= None, password= None):
        self.prefix = prefix
        self.host = host
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


    def insert_file(self, database, path, **kwargs):
        if self.client:
            db = self.client[database]
            grid_db = gridfs.GridFS(db)
            with open(path, "br") as f:
                grid_db.put(f, **kwargs)



    def close_connection(self):
        if self.client:
            self.client.close()
            logger.info(f"connection to mongodb {self.URI} closed")