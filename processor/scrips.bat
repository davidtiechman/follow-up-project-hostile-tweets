docker build -t kafka-consumer .
docker tag kafka-consumer davidtiechman/kafka-consumer:latest
docker push davidtiechman/kafka-consumer:latest
docker pull davidtiechman/kafka-consumer:latest
