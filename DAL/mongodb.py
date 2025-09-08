from pymongo import MongoClient
import gridfs
from pathlib import Path
from logger.logger import Logger
logger = Logger.get_logger()


class DALMongo:

    def __init__(self, prefix, host, database, collection, user= None, password= None):
        """ class for fast connect to collection in mongodb.
            params: The details that make up the mongodb uri,
            name database and name collection that it doesn't matter if they exist or not.
             for use first run open_connection method"""
        self.prefix = prefix
        self.host = host
        self.database = database
        self.collection = collection
        self.user = user
        self.password = password
        self.URI = self.build_URI()
        self.client = None


    def build_URI(self):
        """ build uri in accordance with the data """
        if self.user and self.password:
            URI = f"{self.prefix}://{self.user}:{self.password}@{self.host}::27017"
        else:
            URI = f"{self.prefix}://{self.host}:27017"

        return URI


    def open_connection(self):
        """ create MongoClient connection and checks if the connection was successful
            return bool respectively """
        try:
            self.client = MongoClient(self.URI)
            self.client.admin.command("ping")
            logger.info(f"connected to mongodb {self.URI} - ready for operations")
            return True
        except Exception as e:
            self.client = None
            logger.error(f"Error during try to connect to {self.URI} : {e}")
            return False


    def insert_file(self, source_path, **kwargs):
        """ insert file from source_path to collection by using gridfs library.
            receives path of file for upload him and optional **kwargs to keep with him """
        path = Path(source_path)
        if not path.exists():
            raise FileNotFoundError(f"the path file: {path} does not exists")
        if self.client:
            db = self.client[self.database]
            grid_db = gridfs.GridFS(db, collection=self.collection)
            # open the file and send him to mongodb using grid_db.put method
            with open(source_path, "br") as f:
                grid_db.put(f, **kwargs)


    def load_file(self, file_id, destination_path, new_file_name):
        """ load file from mongodb collection by field id using by gridfs library.
            file_id for identify the desired file, destination path folder and new_file_name for load him. """
        path = Path(destination_path)
        if not path.exists():
            raise FileNotFoundError(f"the path file: {path} does not exists")
        if self.client:
            db = self.client[self.database]
            fs = gridfs.GridFS(db, collection=self.collection)
            grid_out =  fs.find_one({"id": file_id})
            data = grid_out.read()
            with open(f"{destination_path}\\{new_file_name}", "bw") as f:
                f.write(data)


    def close_connection(self):
        """ close the connection """
        if self.client:
            self.client.close()
            self.client = None
            logger.info(f"connection to mongodb {self.URI} closed")



# example
if __name__ == "__main__":
    dal_mongo = DALMongo("mongodb", "localhost", "muezzin", "fs")
    print(dal_mongo.open_connection())
    #data = dal_mongo.load_file("download (10).wav-1979-12-31 23:00:00-1326.18 KB-", "C:\\python_data\\new_podcast", "new10.wav")
