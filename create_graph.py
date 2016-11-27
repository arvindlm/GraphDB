import sys
from time import time
from collections import defaultdict
import zeusdb

PATH = "data/"
person_id = {}

def tsv2list(path):
	data = open(path, "r").read()
	return [[x for x in line.rstrip("\r").split("\t")] for line in data.rstrip("\n").split("\n")]

def bulk_create_nodes(nodes, id_field):
	id_map = {}
	total = len(nodes)
	i = 1
	start_time = time()
	for node in nodes:
		new_id = zeusdb.create_node(node)
		sys.stdout.write("\rCreated "+str(i)+" nodes out of "+str(total)+" nodes")
		sys.stdout.flush()
		id_map[node[id_field]] = new_id
		i += 1
	end_time = time()
	print
	print "It took " + str(end_time-start_time) + " seconds to create " + str(total) + " nodes"
	return id_map

def bulk_create_edges(edges):
	total = len(edges)
	i = 1
	start_time = time()
	for edge in edges:
		zeusdb.create_edge(edge)
		sys.stdout.write("\rCreated "+str(i)+" edges out of "+str(total)+" edges")
		sys.stdout.flush()
		i += 1
	end_time = time()
	print
	print "It took " + str(end_time-start_time) + " seconds to create " + str(total) + " edges"

def create_person_nodes():
	global person_id
	print
	print "Reading person nodes data file"
	person_nodes = tsv2list(PATH+"personNodes.txt")
	person_nodes = [{"id": x[0],
					 "first_name": x[1],
					 "last_name": x[2],
					 "gender": x[3],
					 "age": x[4],
					 "type": "person"
					} for x in person_nodes]

	print "Creating person nodes"
	person_id = bulk_create_nodes(person_nodes, "id")
	print
	create_person_edges()

def create_person_edges():
	print
	print "Reading person edges data file"
	person_edges = tsv2list(PATH+"personEdges.txt")
	person_edges = [{"source": person_id[x[0]],
					 "destination": person_id[x[1]],
					 "type": "friend"
					} for x in person_edges]
	print "Creating person edges"
	bulk_create_edges(person_edges)
	print

def create_location_nodes():
	print
	print "Reading checkin nodes data file"
	checkin_nodes = tsv2list(PATH+"checkins.txt")
	location_nodes = {}
	for node in checkin_nodes:
		if not node[4]:
			continue
		location_nodes[node[4]] = {
									"latitude": node[2],
									"longitude": node[3],
									"location_id": node[4],
									"type": "location"
								}
	location_nodes = location_nodes.values()
	print "Creating location nodes"
	location_map = bulk_create_nodes(location_nodes, "location_id")
	print
	create_location_edges(checkin_nodes, location_map)

def create_location_edges(checkin_nodes, location_map):
	print
	print "Processing location edges data"
	visit_count = defaultdict(lambda: 0)
	for node in checkin_nodes:
		key = node[0] + "==>" + node[4]
		visit_count[key] += 1
	location_edges = []
	for key in visit_count.keys():
		node_ids = key.split("==>")
		location_edges.append({"source": person_id[node_ids[0]],
							   "destination": location_map[node_ids[1]],
							   "visit_count": str(visit_count[key]),
							   "type": "visited"
							})
	print "Creating location edges"
	bulk_create_edges(location_edges)
	print

def main():
	create_person_nodes()
	create_location_nodes()
	print "DONE"
	print

if __name__ == "__main__":
	main()