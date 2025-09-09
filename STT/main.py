from DAL.mongodb import DALMongo
from DAL.elastic_search import DALElastic
from transcription_manager import Transcriber
from configs import elastic_config, mongodb_config


if __name__ == "__main__":
    DAL_mongo = DALMongo(mongodb_config.MONGO_PREFIX, mongodb_config.MONGO_HOST, mongodb_config.MONGO_DB, mongodb_config.MONGO_COLLECTION)
    DAL_elastic = DALElastic(elastic_config.ES_HOST_NAME, elastic_config.ES_INDEX)
    transcriber = Transcriber(DAL_mongo, DAL_elastic)
    transcriber.run_process()