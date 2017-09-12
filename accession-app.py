from optparse import OptionParser

from ingestapi import IngestApi
from accessionprocessor import AccessionProcessor
from messagereceiver import MessageReceiver
import config

if __name__ == '__main__':

    ingest_api = IngestApi(ingest_url=config.INGEST_API_URL)
    print config.INGEST_API_URL
    accession_processor = AccessionProcessor(ingest_api=ingest_api)

    MessageReceiver(host=config.RABBITMQ_HOST,
                    port=config.RABBITMQ_PORT,
                    queue=config.RABBITMQ_ACCESSION_QUEUE,
                    message_processor=accession_processor) 

