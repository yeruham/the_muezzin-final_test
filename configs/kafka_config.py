import os


# kafka variables
KAFKA_SERVER_URI = os.getenv("KAFKA_SERVER_URI", "localhost:9092")
KAFKA_PRODUCER_TOPIC = os.getenv("KAFKA_PRODUCER_TOPIC", "podcast_metadata")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "muezzin-group")
TIME_CONSUMER_LIMITED = 10000