import glob, json, os, urllib, requests, logging
import config

ENTITY_TYPE_LINKS = {
    "sample" : "samples",
    "assay" : "assays",
    "analysis" : "analyses",
    "file": "files",
    "project":"projects",
    "protocol": "protocols"
}

SEARCH_UUID_PATH = '/search/findByUuid?uuid='

class IngestApi:

    def __init__(self, ingest_url=None):
        reply = urllib.urlopen(ingest_url)
        self.links = json.load(reply)['_links']
        self.ingest_url = ingest_url
        
        self.logger = logging.getLogger(__name__)
        self.headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    def update_entity_by_uuid(self, entity_type, uuid, json_str):
        entity_url = self.get_entity_url_by_uuid(entity_type, uuid)
        r = requests.patch(entity_url, data=json_str, headers=self.headers)
        
        if r.status_code != requests.codes.ok:
            self.logger.error(str(r))

    def get_entity_url_by_uuid(self, entity_type, uuid):
        entity_index_url = self.get_entity_index(entity_type)
        entity_find_by_uuid_url = entity_index_url + SEARCH_UUID_PATH + uuid
        entity_response = urllib.urlopen(entity_find_by_uuid_url)
        entity_url = json.load(entity_response)['_links']['self']['href']
        
        return entity_url

    def get_entity_index_url(self, entity_type):
        metadata_type = ENTITY_TYPE_LINKS[entity_type.lower()]
        entity_index_url = self.links[metadata_type]['href'].rsplit('{')[0]
        return entity_index_url

    def update_entity(self, entity_type, entity_id, json_str):
        entity_url = self.get_entity_index_url(entity_type) + '/' + entity_id
        r = requests.patch(entity_url, data=json_str, headers=self.headers)
        
        if r.status_code != requests.codes.ok:
            self.logger.error(str(r))
    