FROM jfloff/alpine-python:2.7-slim
MAINTAINER Simon Jupp "jupp@ebi.ac.uk"

RUN mkdir /app
WORKDIR /app
ADD ingestbroker ./lib
COPY export-to-dss.py requirements.txt ./

RUN pip install -r requirements.txt

ENV INGEST_API=http://localhost:8080
ENV RABBIT_URL=amqp://localhost:5672
ENV SUBMISSION_QUEUE_NAME=ingest.envelope.submitted.queue

ENTRYPOINT ["python"]
CMD ["export-to-dss.py"]
