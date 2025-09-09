from DAL.elastic_search import DALElastic
from text_analysis import num_words_in_text
from classified import Classified
from logger.logger import Logger
logger = Logger.get_logger()


class ClassifiedManager:

    def __init__(self, DAL_elastic: DALElastic, hostile_words, less_hostile_words):
        self.dal_elastic = DAL_elastic
        self.hostile_words = hostile_words
        self.less_hostile_words = less_hostile_words


    def run_process(self):
        if self.dal_elastic.is_connected():
            logger.info(f"ClassifiedManager connected to elastic-index: {self.dal_elastic.host}, "
                        f"start the classified process.")
            documents = self.dal_elastic.get_documents()
            logger.info(f"classified get {len(documents)} documents from elastic")
            for document in documents:
                try:
                    id = document["_id"]
                    text = document["transcribed_text"]
                    print(id)
                    text = text.lower().split(" ")
                    num_hostile_words = num_words_in_text(self.hostile_words, text)
                    num_lass_hostile_words = num_words_in_text(self.less_hostile_words, text)
                    classified = Classified(len(text), num_hostile_words, num_lass_hostile_words)
                    full_risk = classified.full_risk()
                    print(full_risk)
                    self.dal_elastic.update_document(id, full_risk)
                except Exception as e:
                    logger.error(f"Error during try to classified the {document} document: {e}")
        else:
            logger.info(f"Error: classified can't work, because of there is no connection to elastic: {self.dal_elastic.host}.")