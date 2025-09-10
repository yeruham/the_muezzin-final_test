from DAL.elastic_search import DALElastic
from text_analysis import num_words_in_text
from classified import Classified
from logger.logger import Logger
logger = Logger.get_logger()


class ClassifiedManager:

    def __init__(self, dal_elastic: DALElastic, name_filed_in_elastic , hostile_words: dict[int: list]):
        """ manages the classification process of texts stored in elastic-index.
            receives DAl_elastic for connection with elastic,
            name of filed in elastic to be classified,
            dict of lists hostile_words with kwy of level his risk -
            (the final risk calculation will be divided by the level of risk). """
        self.dal_elastic = dal_elastic
        self.name_filed_in_elastic = name_filed_in_elastic
        self.hostile_words = hostile_words


    def run_process(self):
        """ run the process - pulling out all documents from elastic-index, Go through them one by one,
            classifies her and update her risk level back to elastic-index. """
        if self.dal_elastic.is_connected():
            logger.info(f"ClassifiedManager connected to elastic-index: {self.dal_elastic.host}, "
                        f"start the classified process.")
            documents = self.dal_elastic.get_documents()
            logger.info(f"classified get {len(documents)} documents from elastic")
            for document in documents:
                try:
                    doc_id = document["_id"]
                    full_risk = self.classified_document(document)
                    print(f"doc_id: {doc_id} full_risk: {full_risk}")
                    self.dal_elastic.update_document(doc_id, full_risk)
                except Exception as e:
                    logger.error(f"Error during try to classified the {document} document: {e}")
        else:
            logger.info(f"Error: classified can't work, because of there is no connection to elastic: {self.dal_elastic.host}.")


    def classified_document(self, document: dict):
        """ extracts the relevant column from the document, classified her and return its full of risk. """
        text = document[self.name_filed_in_elastic]
        text = text.lower().split(" ")
        full_num_hostile_words_found = 0
        for level_risk, list_words in self.hostile_words.items():
            # calculates how many words were found and divides by the level of danger.
            num_hostile_words_found = num_words_in_text(list_words, text)
            num_hostile_words_found /= level_risk
            full_num_hostile_words_found += num_hostile_words_found
        print(full_num_hostile_words_found)
        classified = Classified(len(text), full_num_hostile_words_found)
        full_risk = classified.full_risk()
        return full_risk