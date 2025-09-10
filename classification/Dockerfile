FROM python:3.11

WORKDIR /app

COPY ./classification/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./classification .
COPY ./logger logger/
COPY ./DAL/ DAL/
COPY ./configs configs/


ENV ES_HOST_NAME="es"
ENV LOGGER_ES_HOST="http://es:9200"


CMD ["python", "main.py"]