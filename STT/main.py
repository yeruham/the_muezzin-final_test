from DAL.mongodb import DALMongo
from DAL.elastic_search import DALElastic
from transcription_manager import Transcriber
from db_uploader import config


if __name__ == "__main__":
    DAL_mongo = DALMongo(config.MONGO_PREFIX, config.MONGO_HOST, config.MONGO_DB, config.MONGO_COLLECTION)
    DAL_elastic = DALElastic(config.HOST_NAME, config.INDEX)
    transcriber = Transcriber(DAL_mongo, DAL_elastic)
    transcriber.run_process()