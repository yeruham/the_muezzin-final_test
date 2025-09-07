from pymongo import MongoClient


class DALMongo:

    def __init__(self, prefix, host, database, collection, user= None, password= None):
        self.prefix = prefix
        self.host = host
        self.database = database
        self.collection = collection
        self.user = user
        self.password = password
        self.URI = self.get_URI()
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
            return True
        except Exception as e:
            self.client = None
            print(f"Error: {e}")
            return False


    def close_connection(self):
        if self.client:
            self.client.close()