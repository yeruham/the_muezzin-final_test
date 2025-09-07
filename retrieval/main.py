from retrieval.manager import Manager
import config

if __name__ == "__main__":
    # init instance of manager with source folder path and kafka env variables from config.py
    manager = Manager(config.SOURCE_FOLDER_PATH,
                      config.KAFKA_SERVER_URI,
                      config.KAFKA_PRODUCER_TOPIC)
    # run process - save all metadata files that in source folder and send them to kafka
    manager.run_process()