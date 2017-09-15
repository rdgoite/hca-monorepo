#!/usr/bin/env python
"""
Listens for messages from ingest to create a staging area, post back the credentials for uploading 
files to the staging area
"""
__author__ = "jupp"
__license__ = "Apache 2.0"
__date__ = "15/09/2017"

import pika
import ingestbroker.broker.stagingapi as stagingapi
import ingestbroker.broker.ingestapi as ingestapi
from optparse import OptionParser
import os, sys
import logging
import json

DEFAULT_RABBIT_URL=os.environ.get('RABBIT_URL', 'amqp://localhost:5672')
DEFAULT_QUEUE_NAME=os.environ.get('SUBMISSION_QUEUE_NAME', 'ingest.envelope.created.queue')

class IngestReceiver:
    def __init__(self, options={}):

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.basicConfig(level=options.log, formatter=formatter)
        self.logger = logging.getLogger(__name__)

        self.rabbit = options.rabbit if options.rabbit else os.path.expandvars(DEFAULT_RABBIT_URL)
        self.logger.debug("rabbit url is "+self.rabbit )

        self.queue = options.queue if options.queue else DEFAULT_QUEUE_NAME
        self.logger.debug("rabbit queue is "+self.queue )

        connection = pika.BlockingConnection(pika.URLParameters(self.rabbit))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue)

        def callback(ch, method, properties, body):
            self.logger.info(" [x] Received %r" % body)
            submittedObject = json.loads(body)
            if "id" in submittedObject:
                submissionId = submittedObject["id"]
                ingestApi = ingestapi.IngestApi()
                subUrl = ingestApi.getSubmissionUri(submissionId)
                uuid = ingestApi.getObjectUuid(subUrl)
                stagingApi = stagingapi.StagingApi()
                submissionCredentials = stagingApi.createStagingArea(uuid)
                ingestApi.updateSubmissionWithStagingCredentials(subUrl, submissionCredentials)

        channel.basic_consume(callback,
                              queue=self.queue,
                              no_ack=True)

        self.logger.info(' [*] Waiting for messages from submission envelope')
        channel.start_consuming()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    parser = OptionParser()
    parser.add_option("-q", "--queue", help="name of the ingest queues to listen for submission")
    parser.add_option("-r", "--rabbit", help="the URL to the Rabbit MQ messaging server")
    parser.add_option("-l", "--log", help="the logging level", default='INFO')

    (options, args) = parser.parse_args()
    IngestReceiver(options)
