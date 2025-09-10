import base64
from DAL.elastic_search import DALElastic
from classified_manager import ClassifiedManager
from configs import elastic_config
import os


NAME_FIELD_FOR_CLASSIFIED = os.getenv("NAME_FIELD_FOR_CLASSIFIED", "transcribed_text")
# two encode hostile-words
ENCODE_HOSTILE_WORDS = "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT"
ENCODE_LESS_HOSTILE_WORDS = "RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=="


def b64decode(encode_text):
    decode_text = base64.b64decode(encode_text).decode('utf-8')
    return decode_text



if __name__ == "__main__":
    # deciphering the both lists, converts the strings to lowercase, and split them by commas.
    hostile_words = b64decode(ENCODE_HOSTILE_WORDS).lower().split(",")
    lass_hostile_words = b64decode(ENCODE_LESS_HOSTILE_WORDS).lower().split(",")
    # enters the lists into dict by their level
    hostile_words_by_level = {1: hostile_words , 2: lass_hostile_words}
    # init DALElastic with variables from elastic_config
    DAL_elastic = DALElastic(elastic_config.ES_HOST_NAME, elastic_config.ES_INDEX)

    # init the classified and run the process -
    # pulling out data from elastic-index, classified the text and update the elastic be full-risk
    classified = ClassifiedManager(DAL_elastic, NAME_FIELD_FOR_CLASSIFIED, hostile_words_by_level)
    classified.run_process()