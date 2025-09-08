import os


# kafka variables
KAFKA_SERVER_URI = os.getenv("KAFKA_SERVER_URI", "localhost:9092")
KAFKA_PRODUCER_TOPIC = os.getenv("KAFKA_PRODUCER_TOPIC", "podcast_metadata")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "muezzin-group")
TIME_CONSUMER_LIMITED = 10000

# env variables for mongodb, initialized with current mongodb details
MONGO_PREFIX = os.getenv("MONGO_PREFIX", "mongodb")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_USER = os.getenv("MONGO_USER", None)
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", None)
MONGO_DB = os.getenv("MONGO_DB", "muezzin")

# env variables for elasticsearch, initialized with current mongodb details
HOST_NAME = os.getenv("HOST_NAME", "localhost")
INDEX = "muezzin"
MAPPINGS = {"properties":{
        "name": {"type": "keyword"},
        "size": {"type": "keyword"},
        "creation_date": {"type": "keyword"},
        "modified_date": {"type": "keyword"},
        "last_access_date": {"type": "keyword"}
    }}
