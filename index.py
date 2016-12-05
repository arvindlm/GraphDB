from elasticsearch import Elasticsearch
from elasticsearch import helpers
from cassandra.cluster import Cluster
import json
import requests

KEYSPACE = "sample"
cluster = Cluster()
session = cluster.connect(KEYSPACE)

es = Elasticsearch()

NO_OF_SHARDS = 1
NO_OF_REPLICAS = 1
index_data = {}
#maximum size of data to be returned from elastic search query
SIZE = 1000000

with open('index_data.json') as fp:
    index_data = json.load(fp)


# CREATES AN INDEX GIVEN AN INDEX NAME, TYPE OF MAPPING, AND PROPERTIES.
def create_index(name, doc_type, properties, table):
    body,prop_str = create_property_mapping(table, doc_type, properties)
    if body != None:
        if es.indices.exists(name):
            print "ERROR: An index with the provided name already Exists"
            return
        es.indices.create(name, body)
        update_index_data(name, table, doc_type)
        set_result_size(name, SIZE)
        add_records_to_index(name, doc_type, table, prop_str)

def update_index_data(name, table, doc_type):
    index_data[table]["index_info"].append([name, doc_type])
    print index_data
    with open('index_data.json', 'w') as fp:
        json.dump(index_data, fp)

def flush_index_data():
    index_data = {
        "node": {
            "index_info": [],
            "index_fields": []
        },
        "edge": {
            "index_info": [],
            "index_fields": []
        }
    }
    with open('index_data.json', 'w') as fp:
        json.dump(index_data, fp)

def create_sample_json(name, doc_type, id):
    return {
        "_index": name,
        "_type": doc_type,
        "_id": id,
        "name": str(id),
        "age": str(id)
    }
'''
def add_records_to_index(index_name, doc_type, table, prop_str):
    json = []
    for i in range(0, 10):
        json.append(create_sample_json(index_name, doc_type, i))

    helpers.bulk(es, json)
'''
def is_field_indexed(table, field):
    fields = index_data[table]["index_fields"]
    if fields != None:
        for f in fields:
            if f == field:
                return True
    return False

def get_index_info(table):
    return index_data[table]["index_info"]

#def add_record_to_index(table, body):
#    indices = get_index_info(table)
#    if indices != None:
#        for ind in indices:
#            es.create(ind[0], ind[1], body['zid'], get_record_json_from_dict(body, ind[0], ind[1]))
def add_records_to_index(index_name, doc_type, table, prop_str):
    query = "SELECT " + prop_str + " FROM " + table
    rows = session.execute(query)
    count = 0
    json = []
    for row in rows:
        count += 1
        json.append(get_record_json_from_row(row, table, index_name, doc_type))
    helpers.bulk(es, json)
    print count



# RETURNS JSON BODY AND PROPERTY STRING USED FOR QUERYING
def create_property_mapping(table, doc_type, properties):
    res = get_new_index_json()
    prop_str = ""
    for prop in properties:
        res["mappings"][doc_type] = {
            "properties": {
                prop[0] : {
                    "type": prop[1]
                }
            }
        }
        prop_str += prop[0] + ","
        index_data[table]["index_fields"].append(prop[0])
    return res, prop_str + "zid"

def get_record_json_from_dict(props, table, name, doc_type):
    fields = props.keys()
    res = {}
    if name is not None:
        res["_index"] = name
        res["_type"] = doc_type
    for field in fields:
    	val = props[field]
    	if val != None:
            if field in index_data[table]["index_fields"]:
                if field == "zid":
                    field = "_id"
                res[field] = val
    return res

def get_record_json_from_row(row, table, name, doc_type):
    fields = row._fields
    res = {}
    if name is not None:
        res["_index"] = name
        res["_type"] = doc_type
    for field in fields:
        val = getattr(row, field)
        if val != None:
            if field in index_data[table]["index_fields"]:
                if field == "zid":
                    field = "_id"
                res[field] = val
    return res

def set_result_size(index, size):
    if len(index) > 0:
        index += '/'
    url = "http://localhost:9200/" + index + "_settings"
    print url, size
    payload = '{ "index" : { "max_result_window" : 1000000 } }'
    print payload
    print requests.put(url, data=payload)

set_result_size("edge_index15", SIZE)
def search_all_indexes(table, body):
    indices = get_index_info(table)
    print len(indices)
    res = set()
    for index in indices:
        print index
        res = search(body, index[0], "")
    return res

def search(body, index, doc_type):
    res_ids = set()
    print index
    res = es.search(index=index, doc_type=doc_type, body=body, size = SIZE)
    hits = res['hits']['hits']
    for hit in hits:
        res_ids.add(hit['_id'])
    return res_ids

def build_query_json(property_name, property_value):
    return {
        "query": {
            "bool": {
                "should": [
                    { "match": { property_name: property_value }}
                    ]
            }
        }
    }

def flush_index_data():
    index_data = {
        "node": {
            "index_info": [],
            "index_fields": []
        },
        "edge": {
            "index_info": [],
            "index_fields": []
        }
    }
    with open('index_data.json', 'w') as fp:
        json.dump(index_data, fp)

def get_new_index_json():
    return {
        "settings": {
            "index": {
                "number_of_shards": NO_OF_SHARDS,
                "number_of_replicas": NO_OF_REPLICAS
            }
        },
        "mappings" : {}
    }

#TESTING

sample_props = [("name", "text"), ("age", "text")]
search_query = {
    "query": {
        "bool": {
            "should": [
                { "match": { "name": "1" }}

            ]
        }
    }
}
#create_index("sample20", "type13", sample_props, "node")
#print index_fields
#print search(search_query, "sample5", "type4")
#es.create("sample7", "type6", "90", create_sample_json("", "", ""))
