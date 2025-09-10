FROM python:3.11

WORKDIR /app

COPY ./db_uploader/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./db_uploader .
COPY ./kafka_tools kafka_tools/
COPY ./logger logger/
COPY ./DAL/ DAL/
COPY ./configs configs/

ENV KAFKA_SERVER_URI="broker:9092"
ENV ES_HOST_NAME="es"
ENV LOGGER_ES_HOST="http://es:9200"
ENV MONGO_HOST="mongodb"

CMD ["python", "main.py"]