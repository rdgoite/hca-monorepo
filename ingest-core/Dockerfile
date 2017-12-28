FROM openjdk:8-alpine

WORKDIR /opt

ENV LC_ALL=C
ENV MONGO_URI=mongodb://localhost:27017/admin
ENV RABBIT_HOST=localhost
ENV RABBIT_PORT=5672

COPY build/libs/ingest-core.jar ./

CMD java -jar build/libs/*.jar --spring.data.mongodb.uri=$MONGO_URI --spring.rabbitmq.host=$RABBIT_HOST --spring.rabbitmq.port=$RABBIT_PORT
