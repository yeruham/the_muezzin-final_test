from manager import UploadManager
import config


if __name__ == "__main__":
    upload_manager = UploadManager()
    upload_manager.create_dal_mongodb(config.MONGO_PREFIX, config.MONGO_HOST)
    upload_manager.create_dal_elastic(config.HOST_NAME, config.INDEX)
    upload_manager.create_consumer(config.KAFKA_SERVER_URI, config.KAFKA_CONSUMER_GROUP, config.KAFKA_PRODUCER_TOPIC)
    upload_manager.run_process(config.MONGO_DB, config.TIME_CONSUMER_LIMITED)