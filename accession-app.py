from optparse import OptionParser

from ingestapi import IngestApi
from accessionprocessor import AccessionProcessor
from messagereceiver import MessageReceiver
import config

if __name__ == '__main__':
    print config.INGEST_API_URL
    ingest_api = IngestApi(ingest_url=config.INGEST_API_URL)
    
    accession_processor = AccessionProcessor(ingest_api=ingest_api)

    MessageReceiver(url=config.RABBITMQ_URL,
                    queue=config.RABBITMQ_ACCESSION_QUEUE,
                    message_processor=accession_processor) 

