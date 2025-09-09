from pathlib import Path
from speach_to_text import convert_audio_file_to_text
from DAL.mongodb import DALMongo
from DAL.elastic_search import DALElastic
from logger.logger import Logger
logger = Logger.get_logger()


class Transcriber:

    def __init__(self, DAL_mongodb: DALMongo, DAL_elastic: DALElastic):
        """ class Transcriber responsible on transcription of audio files which are stored on mongodb collection,
            and their metadata stored on elastic index.

            in order for it to work it Is necessary get DAL for both of them - mongodb and elastic.

            for start the work run the run_process method """

        if not isinstance(DAL_mongodb, DALMongo) or not isinstance(DAL_elastic, DALElastic):
            raise ValueError(f"one of the objects is not the correct type. current DAL_mongodb is {type(DAL_mongodb)}, "
                             f"and must to be DALMongo. current DAL_elastic is {type(DAL_elastic)}, "
                             f"and must to be DALElastic.")
        self.mongodb = DAL_mongodb
        self.elastic = DAL_elastic
        # creator if not exists the data folder, necessary for storage temp files for transcribe them
        self.data_folder = self._create_data_folder()


    def start_connections(self):
        """ start the connections. in addition makes sure that both DAL connected, and ready for use. """
        connected_to_mongodb = self.mongodb.open_connection()
        connected_to_elastic = self.elastic.is_connected()
        return connected_to_mongodb and connected_to_elastic


    def stop_connections(self):
        self.mongodb.close_connection()


    def run_process(self):
        """ run the transcription process. first pulls the file id's from the elastic-index.
            after that run in a loop on the id's, and for all file id run the self.transcriber_process -
            which download the file, transcribing it, and save the transcript on elastic back """
        connected_to_dbs = self.start_connections()
        if connected_to_dbs:
            logger.info(f"Transcriber connected to elastic: {self.elastic.host} and to mongodb: {self.mongodb.URI}. "
                        f"begins the download - transcription - storage process. ")
            # list from elastic with all the id's files
            id_of_files = self.elastic.get_only_id_of_all_documents()
            logger.info(f"{len(id_of_files)} files id's finds in elastic-index: {self.elastic.index}.")
            num_successfully_transcribed = 0
            for file_id in id_of_files:
                process_work = self.transcriber_process(file_id)
                if process_work:
                    num_successfully_transcribed += 1
            logger.info(f"{num_successfully_transcribed} files have been transcribed, "
                        f"and were successfully added to elastic")

        else:
            logger.error("Error: Transcriber cannot work because of one of connections to dbs not working.")

        self.stop_connections()


    def transcriber_process(self, file_id):
        """  download  file from mongodb-collection by file_id,
            saves the file temporarily in a folder \data, transcribes the file,
            send the transcribed text back to elastic-index. finally remove the temp file. """
        temp_file_name = "temp_file"
        try:
            self.mongodb.load_file(file_id, self.data_folder, temp_file_name)
            audio_path = self.data_folder.joinpath(temp_file_name)
            transcribed_text = convert_audio_file_to_text(str(audio_path))
            self.elastic.update_user(file_id, {"transcribed_text": transcribed_text})
            logger.info(f"the file {file_id} download, Transcribed successfully, and the text saved in elastic. ")
            # delete the temp file
            audio_path.unlink()
            return True
        except Exception as e:
            logger.error(f"Error during the Transcriber process of file: {file_id}:  {e}")
            return False


    def _create_data_folder(self):
        data_folder = Path(".\\data")
        if not data_folder.exists():
            Path.mkdir(data_folder)
        return data_folder