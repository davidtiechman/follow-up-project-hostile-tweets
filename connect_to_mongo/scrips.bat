docker build -t insert-to-mongo .
docker tag insert-to-mongo davidtiechman/kafka-consumer:latest
docker push davidtiechman/insert-to-mongo:latest
docker pull davidtiechman/insert-to-mongor:latest
