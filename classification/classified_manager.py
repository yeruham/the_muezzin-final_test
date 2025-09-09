from DAL.elastic_search import DALElastic
from text_analysis import num_words_in_text
from classified import Classified


class ClassifiedManager:

    def __init__(self, DAL_elastic: DALElastic, hostile_words, less_hostile_words):
        self.dal_elastic = DAL_elastic
        self.hostile_words = hostile_words
        self.less_hostile_words = less_hostile_words


    def run_process(self):
        if self.dal_elastic.is_connected():
            documents = self.dal_elastic.get_documents()
            for document in documents:
                id = document["_id"]
                text = document["transcribed_text"]
                print(id)
                text = text.split(" ")
                num_hostile_words = num_words_in_text(self.hostile_words, text)
                num_lass_hostile_words = num_words_in_text(self.less_hostile_words, text)
                classified = Classified(len(text), num_hostile_words, num_lass_hostile_words)
                full_risk = classified.full_risk()
                print(full_risk)
                self.dal_elastic.update_document(id, full_risk)