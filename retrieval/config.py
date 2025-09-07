import os


SOURCE_FOLDER_PATH = os.getenv("SOURCE_FOLDER_PATH", "C:\python_data\podcasts")
KAFKA_SERVER_URI = os.getenv("KAFKA_SERVER_URI", "localhost:9200")
KAFKA_PRODUCER_TOPIC = os.getenv("KAFKA_PRODUCER_TOPIC", "podcast_metadata")