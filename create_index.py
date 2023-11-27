from elasticsearch import Elasticsearch

elastic = Elasticsearch([{'host': 'localhost', 'port': 9200}])
elastic.indices.create(index='yass')
print(elastic.indices.get_alias().keys())
print(elastic.info())
