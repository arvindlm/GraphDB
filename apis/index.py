from elasticsearch import Elasticsearch
from elasticsearch import helpers
from cassandra.cluster import Cluster
import json
import requests

KEYSPACE = "zeus"
cluster = Cluster(['54.218.56.39'])
session = cluster.connect(KEYSPACE)

es = Elasticsearch()

NO_OF_SHARDS = 1
NO_OF_REPLICAS = 1
index_data = {}
#maximum size of data to be returned from elastic search query
SIZE = 1000000

with open('/home/ubuntu/GraphDB/apis/index_data.json') as fp:
    index_data = json.load(fp)


# CREATES AN INDEX GIVEN AN INDEX NAME, TYPE OF MAPPING, AND PROPERTIES.
def create_index(name, doc_type, properties, table):
    body,prop_str = create_property_mapping(table, doc_type, properties)
    print body
    if body != None:
        if es.indices.exists(name):
            print "ERROR: An index with the provided name already Exists"
            return
        es.indices.create(name, body)
        update_index_data_file(name, table, doc_type)
        set_result_size(name, SIZE)
        add_records_to_index(name, doc_type, table, prop_str)


#add single record to index
def add_record_to_index(table, body):
    indices = get_index_info(table)
    if indices != None:
        for ind in indices:
            es.create(ind[0], ind[1], body['zid'], get_record_json_from_dict(body, ind[0], ind[1]))

#add multiple records to index from table. Called when creating an index
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

#delete record based on query
def delete_record_from_index(node_id):
	print node_id
	query = {
    		"query": {
            			"term": {"zid": node_id }
    		}
	}
	es.delete_by_query(index="_all", doc_type="", body=query)


# RETURNS JSON BODY AND PROPERTY STRING USED FOR QUERYING
def create_property_mapping(table, doc_type, properties):
    res = get_new_index_json()
    prop_str = ""
    for prop in properties:
        res["mappings"][doc_type] = {
            "properties": {
                "zid" : {
                    "type": "text",
		    "index": "not_analyzed"
                }
            }
        }
        prop_str += prop[0] + ","
        index_data[table]["index_fields"].append(prop[0])
    return res, prop_str + "zid"

#Search all indexes of a table
def search_all_indexes(table, body):
    indices = get_index_info(table)
    print len(indices)
    res = set()
    for index in indices:
        print index
        res = search(body, index[0], "")
    return res

#Search a particular index and doc_type
def search(body, index, doc_type):
    res_ids = set()
    res = es.search(index=index, doc_type=doc_type, body=body, size = SIZE)
    hits = res['hits']['hits']
    for hit in hits:
        res_ids.add(hit['_source']['zid'])
    return res_ids

# set the number of results that need to be returned(pagination)
def set_result_size(index, size):
    if len(index) > 0:
        index += '/'
    url = "http://localhost:9200/" + index + "_settings"
    print url, size
    payload = '{ "index" : { "max_result_window" : %d } }' % size
    print payload
    print requests.put(url, data=payload)

def get_index_info(table):
    return index_data[table]["index_info"]

def is_field_indexed(table, field):
    fields = index_data[table]["index_fields"]
    if fields != None:
        for f in fields:
            if f == field:
                return True
    return False

def update_index_data_file(name, table, doc_type):
    index_data[table]["index_info"].append([name, doc_type])
    print index_data
    with open('index_data.json', 'w') as fp:
        json.dump(index_data, fp)

#JSON BUILDERS

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
               # if field == "zid":
               #     field = "_id"
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
            res[field] = val
    return res


def build_query_json(properties):
    query = {"query": {"bool" : { "should": [] } }}

    for prop in properties:
        query["query"]["bool"]["should"].append({"match" : {prop : properties[prop]}})
    return query

def flush_index_data_file():
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
        "mappings" : {

	}
    }
