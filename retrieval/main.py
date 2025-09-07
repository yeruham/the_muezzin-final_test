from retrieval.manager import Manager
import config

if __name__ == "__main__":
    manager = Manager(config.SOURCE_FOLDER_PATH,
                      config.KAFKA_SERVER_URI,
                      config.KAFKA_PRODUCER_TOPIC)
    manager.run_process()