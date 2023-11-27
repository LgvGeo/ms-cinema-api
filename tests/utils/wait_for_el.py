import time

from elasticsearch import Elasticsearch

from tests.settings import ElasticsearchSettings

if __name__ == '__main__':
    elastic_conf = ElasticsearchSettings()
    es_client = Elasticsearch(
        hosts=[f'{elastic_conf.host}:{elastic_conf.port}'])
    while True:
        if es_client.ping():
            break
        time.sleep(1)
