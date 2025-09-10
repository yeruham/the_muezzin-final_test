from pathlib import Path
from file_metadata import FileMetadata
from kafka_tools.producer import Producer
from logger.logger import Logger
logger = Logger.get_logger()


class Manager:

    def __init__(self, source_folder_path, kafka_server_uri, topic):
        """ class who manages the retrieval plan - initialized with source_folder_path
            and kafka producer details (kafka server and topic name) """
        self.path = Path(source_folder_path)
        self.kafka_server_uri = kafka_server_uri
        self.topic = topic


    def get_subfiles(self):
        """ return list with absolute paths of sub files from self.path """
        # if self.path.exists() and self.path.is_dir():
        subfiles_paths = []
        for sub in self.path.iterdir():
            subfiles_paths.append(sub)
        return subfiles_paths



    def get_kafka_producer(self):
        """ return kafka-producer by self.kafka_server_uri """
        producer = Producer(self.kafka_server_uri)
        producer.create_producer()
        return producer


    def run_process(self):
        """ ron the process - first get all sub files from path and create kafka-producer.
         than get metadata and send him to kafka for all one of them """
        logger.info("retrieval process start")
        subfiles_paths = self.get_subfiles()
        producer = self.get_kafka_producer()
        for path in subfiles_paths:
            try:
                # use with FileMetadata class to access easily to metadata
                file_metadata = FileMetadata(path)
                metadata = file_metadata.full_metadata()
                metadata.update({"path": path})
                print(f"send metadata of file {path}")
                producer.publish_messages(self.topic, metadata)
            except Exception as e:
                logger.error(f"Error while trying to access metadata of {path}: {e}")
        logger.info(f"finished sending to kafka topic {self.topic} {len(subfiles_paths)} messages")
        # flush the messages and close the producer
        producer.flush_messages()
        producer.close_producer()
        logger.info("retrieval process ended")
        print("finish to send all data")