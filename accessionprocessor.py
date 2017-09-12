import pika, logging, uuid, json


class AccessionProcessor:
    def __init__(self, ingest_api):
        self.ingest_api = ingest_api
        self.logger = logging.getLogger(__name__)

    def run(self, message):
        params = json.loads(message)
        
        accession_no = str(uuid.uuid4())
        debug_message = 'New Accession Number {accession_no}'.format(accession_no=accession_no)
        self.logger.info(debug_message)
        
        metadata_update = {}
        metadata_update['accession'] = {}
        metadata_update['accession']['number'] = accession_no
        
        metadata_uuid = params['uuid']['uuid']
        metadata_entity_type = params['entityType']
        self.ingest_api.update_entity_by_uuid(metadata_entity_type, metadata_uuid, json.dumps(metadata_update))
        self.logger.info('updated entity by uuid!')