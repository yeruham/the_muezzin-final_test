import os


# env variables for mongodb, initialized with current mongodb details
MONGO_PREFIX = os.getenv("MONGO_PREFIX", "mongodb")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_USER = os.getenv("MONGO_USER", None)
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", None)
MONGO_DB = os.getenv("MONGO_DB", "muezzin")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "podcast")