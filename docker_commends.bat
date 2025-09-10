docker network create muezzin-net

docker run -d --name mongodb --network muezzin-net -p 27017:17017 mongo:latest

docker run -d --name broker --network muezzin-net -e KAFKA_NODE_ID=1 -e KAFKA_PROCESS_ROLES=broker,controller -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://broker:9092   -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER   -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT   -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@broker:9093   -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1  -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1  -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1   -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0  -e KAFKA_NUM_PARTITIONS=3  apache/kafka:latest

docker run -d --name es -p 9200:9200 --network muezzin-net -e "discovery.type=single-node"  -e "xpack.security.enabled=false"  -e "ES_JAVA_OPTS=-Xms1g -Xmx1g"  docker.elastic.co/elasticsearch/elasticsearch:8.15.0

docker build -f .\retrieval\Dockerfile   -t retrieval .
docker run -d --name retrieval --network muezzin-net  --mount type=bind,src=C:\\python_data\\podcasts,dst=app/data retrieval

docker build -f .\db_uploader\Dockerfile   -t db_uploader .
docker run -d --name db_uploader --network muezzin-net  --mount type=bind,src=C:\\python_data\\podcasts,dst=/app/data db_uploader

docker build -f ".\stt\Dockerfile"   -t stt .
 docker run -d --name stt --network muezzin-net  stt

docker build -f ".\classification\Dockerfile"   -t classification .
 docker run -d --name classification--network muezzin-net  classification
