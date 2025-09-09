from manager import UploadManager
import config
from configs import elastic_config, mongodb_config, kafka_config


if __name__ == "__main__":
    upload_manager = UploadManager()
    upload_manager.create_dal_mongodb(mongodb_config.MONGO_PREFIX, mongodb_config.MONGO_HOST, mongodb_config.MONGO_DB, mongodb_config.MONGO_COLLECTION)
    upload_manager.create_dal_elastic(elastic_config.ES_HOST_NAME, elastic_config.ES_INDEX)
    upload_manager.create_consumer(kafka_config.KAFKA_SERVER_URI, kafka_config.KAFKA_CONSUMER_GROUP, kafka_config.KAFKA_PRODUCER_TOPIC)
    upload_manager.run_process(mongodb_config.MONGO_DB, kafka_config.TIME_CONSUMER_LIMITED)