import os


LOGGER_NAME = os.getenv("LOGGER_NAME", "logger-muezzin")
LOGGER_ES_HOST = os.getenv("LOGGER_ES_HOST", "http://localhost:9200")
LOGGER_ES_INDEX = os.getenv("LOGGER_ES_INDEX", "logging-muezzin")