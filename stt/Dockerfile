FROM python:3.11

WORKDIR /app

COPY ./stt/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./stt .
COPY ./logger logger/
COPY ./DAL/ DAL/
COPY ./configs configs/


ENV ES_HOST_NAME="es"
ENV LOGGER_ES_HOST="http://es:9200"
ENV MONGO_HOST="mongodb"

CMD ["python", "main.py"]