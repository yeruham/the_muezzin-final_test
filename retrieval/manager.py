from pathlib import Path
from get_metadata import FileMetadata
from kafka_tools.producer import Producer


class Manager:

    def __init__(self, source_folder_path, kafka_server_uri, topic):
        """ class who manages the retrieval plan - initialized with source_folder_path
            and kafka producer details (kafka server and topic name) """
        self.path = Path(source_folder_path)
        self.kafka_server_uri = kafka_server_uri
        self.topic = topic


    def _get_metadata(self, path_file):
        """ internal method which accepts path of file and return dict with all his metadata """
        try:
            # use with FileMetadata class to access easily to metadata
            metadata_file = FileMetadata(path_file)
            metadata = {"path": metadata_file.path_file,
                        "name": metadata_file.name(),
                        "size": metadata_file.size(),
                        "creation_date": metadata_file.creation_date(),
                        "modified_date": metadata_file.modified_date(),
                        "last_access_date": metadata_file.last_access_date()}
            return metadata
        except Exception as e:
            print(f"Error while trying to access metadata of {path_file}: {e}")
            return None


    def get_subfiles(self):
        """ return list with absolute paths of sub files from self.path """
        if self.path.exists() and self.path.is_dir():
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
        subfiles_paths = self.get_subfiles()
        producer = self.get_kafka_producer()
        for path in subfiles_paths:
            metadata_of_file = self._get_metadata(path)
            if metadata_of_file:
                print(f"send {metadata_of_file["name"]}")
                producer.publish_messages(self.topic, metadata_of_file)
        # flush the messages and close the producer
        producer.flush_messages()
        producer.close_producer()
        print("finish to send all data")