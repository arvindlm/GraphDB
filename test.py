import index
import zeusdb_temp
from time import time

node_properties_1 = [
    ("first_name","text"),
    ("last_name", "text"),
    ("gender", "text"),
    ("age", "text"),
    ("type", "text")

]
node_properties_2 = [
   ("gender", "text"),
    ("age", "text")
]
node_properties_3 = [
    ("gender", "text")
]
node_properties_4 = [
    ("first_name", "text")
]
edge_properties_1 = {
    "source": "text",
    "destination": "text",
    "type": "text"
}
edge_properties_2 = [
    ("type", "text"),
    ("destination", "text")
]
person_node = {
    "id": "Afds",
	"first_name": "Arvind",
	"last_name": "ds",
	"gender": "M",
	"age": "16",
	"type": "person"

}
person_node_2 = {
    "id": "Afdg",
	"first_name": "Ara",
	"last_name": "ds",
	"gender": "M",
	"age": "16",
	"type": "person"

}
person_edges = {
    "source": "afds",
    "destination": "afdg",
    "type": "friend"
}
'''
start_time = time()
index.create_index("node_index10", "test_type2", node_properties_2, zeusdb_temp.NODE_TABLE)
end_time = time()
print "Create Node Index total time : " + str(end_time - start_time)
'''
#start_time = time()
#index.create_index("edge_index17", "test_type2", edge_properties_2, zeusdb_temp.EDGE_TABLE)
#end_time = time()
#print "Create Edge Index total time : " + str(end_time - start_time)

#zeusdb_temp.create_node(person_node, True)
#zeusdb_temp.create_node(person_node_1, True)
#zeusdb_temp.create_edge(props, True)

#start_time = time()
#zeusdb_temp.get_object_by_property(zeusdb_temp.NODE_TABLE, "gender", "M")
#end_time = time()
#print "Get Node By Property without indexing : " + str(end_time - start_time)

#start_time = time()
#zeusdb_temp.get_object_by_property(zeusdb_temp.NODE_TABLE, "gender", "Male", True)
#end_time = time()
#print "Get Node By Property with indexing :" + str(end_time - start_time)

#start_time = time()
#zeusdb_temp.get_object_by_property(zeusdb_temp.EDGE_TABLE, "type", "friend")
#end_time = time()
#print "Get Edge By Property without indexing :" + str(end_time - start_time)
start_time = time()
zeusdb_temp.get_object_by_property(zeusdb_temp.EDGE_TABLE, "type", "friend", True)
end_time = time()
print "Get Edge By Property with indexing :" + str(end_time - start_time)


