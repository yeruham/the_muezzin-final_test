import os


# env variables for elasticsearch, initialized with current mongodb details
ES_HOST_NAME = os.getenv("ES_HOST_NAME", "localhost")
ES_INDEX = "muezzin"
ES_MAPPINGS = {"properties":{
        "name": {"type": "keyword"},
        "size": {"type": "keyword"},
        "creation_date": {"type": "keyword"},
        "modified_date": {"type": "keyword"},
        "last_access_date": {"type": "keyword"}
    }}