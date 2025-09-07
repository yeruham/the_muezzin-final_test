from pathlib import Path
from get_metadata import FileMetadata
from kafka_tools.producer import Producer


class Manager:

    def __init__(self, source_folder_path, kafka_server_uri, topic):
        self.path = Path(source_folder_path)
        self.kafka_server_uri = kafka_server_uri
        self.topic = topic


    @staticmethod
    def _get_metadata(path_file):
        metadata_file = FileMetadata(path_file)
        metadata = {"path": metadata_file.path_file,
                    "name": metadata_file.name(),
                    "size": metadata_file.size(),
                    "creation_date": metadata_file.creation_date(),
                    "modified_date": metadata_file.modified_date(),
                    "last_access_date": metadata_file.last_access_date()}
        return metadata


    def get_subfiles(self):
        if self.path.exists() and self.path.is_dir():
            subfiles_paths = []
            for sub in self.path.iterdir():
                subfiles_paths.append(sub)
            return subfiles_paths


    def get_kafka_producer(self):
        producer = Producer(self.kafka_server_uri)
        producer.create_producer()
        return producer


    def run_process(self):
        subfiles_paths = self.get_subfiles()
        producer = self.get_kafka_producer()
        for path in subfiles_paths:
            metadata_of_file = self._get_metadata(path)
            print(f"send {metadata_of_file["name"]}")
            producer.publish_messages(self.topic, metadata_of_file)




