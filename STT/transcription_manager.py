from pathlib import Path
from speach_to_text import convert_audio_file_to_text
from DAL.mongodb import DALMongo
from DAL.elastic_search import DALElastic
from logger.logger import Logger
logger = Logger.get_logger()


class Transcriber:

    def __init__(self, DAL_mongodb: DALMongo, DAL_elastic: DALElastic):
        if not isinstance(DAL_mongodb, DALMongo) or not isinstance(DAL_elastic, DALElastic):
            raise ValueError(f"one of the objects is not the correct type. current DAL_mongodb is {type(DAL_mongodb)}, "
                             f"and must to be DALMongo. current DAL_elastic is {type(DAL_elastic)}, "
                             f"and must to be DALElastic.")
        self.mongodb = DAL_mongodb
        self.elastic = DAL_elastic


    def start_connections(self):
        connected_to_mongodb = self.mongodb.open_connection()
        connected_to_elastic = self.elastic.is_connected()
        return connected_to_mongodb and connected_to_elastic


    def stop_connections(self):
        self.mongodb.close_connection()


    def run_process(self):
        connected_to_dbs = self.start_connections()
        if connected_to_dbs:
            id_of_files = self.elastic.get_only_id_of_all_documents()
            temp_folder = Path(".\\data")
            temp_file_name = "temp_file"
            for file_id in id_of_files:
                try:
                    print(file_id)
                    self.mongodb.load_file(file_id, temp_folder, temp_file_name)
                    audio_path = str(temp_folder.joinpath(temp_file_name))
                    print(audio_path)
                    transcribed_text = convert_audio_file_to_text(audio_path)
                    self.elastic.update_user(file_id, {"transcribed_text": transcribed_text})
                except Exception as e:
                    print(e)

        else:
            logger.error("Error: Transcriber cannot work because of one of connections to dbs not working.")

        self.stop_connections()
