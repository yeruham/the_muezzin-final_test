from manager import Manager
from configs import kafka_config
import os

# the folder from which we extracted the files
SOURCE_FOLDER_PATH = os.getenv("SOURCE_FOLDER_PATH", "C:\\python_data\\podcasts")

if __name__ == "__main__":
    # init instance of manager with source folder path and kafka env variables from configs
    manager = Manager(SOURCE_FOLDER_PATH,
                      kafka_config.KAFKA_SERVER_URI,
                      kafka_config.KAFKA_PRODUCER_TOPIC)
    # run process - save all metadata files that in source folder and send them to kafka
    manager.run_process()