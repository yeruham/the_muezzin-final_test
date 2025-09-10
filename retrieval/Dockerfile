FROM python:3.11

WORKDIR /app

COPY ./retrieval/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./retrieval .
COPY ./kafka_tools kafka_tools/
COPY ./logger logger/
COPY ./DAL/elastic_search.py DAL/elastic_search.py

ENV KAFKA_SERVER_URI="broker:9092"
ENV LOGGER_ES_HOST="http://es:9200"
ENV SOURCE_FOLDER_PATH="./data"

CMD ["python", "main.py"]