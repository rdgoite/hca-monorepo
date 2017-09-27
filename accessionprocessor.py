import logging, uuid, json, time



class AccessionProcessor:

    def __init__(self, ingest_api):
        self.ingest_api = ingest_api
        self.logger = logging.getLogger(__name__)

    def run(self, message):
        params = json.loads(message)

        metadata_uuid = params['documentUuid']

        if not metadata_uuid:
            new_uuid = str(uuid.uuid4())
            debug_message = 'New Accession Number {new_uuid}'.format(new_uuid=new_uuid)
            self.logger.info(debug_message)
            
            metadata_update = {}
            metadata_update['uuid'] = {}
            metadata_update['uuid']['uuid'] = new_uuid
            
            entity_id = params['documentId']
            entity_type = params['documentType']
            entity_link = params['callbackLink']

            time.sleep(1)

            if(self.ingest_api.update_entity_if_match(entity_link, json.dumps(metadata_update))):
                self.logger.info('updated entity accession uuid!')


        else:
            self.logger.info('no update')