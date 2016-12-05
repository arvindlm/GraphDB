from collections import defaultdict

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
	return checkin_nodes, location_map

def create_location_edges(checkin_nodes, location_map):
	print
	print "Processing location edges data"
	person_id_map = utils.read_id_map('person_id_map.txt')
	visit_count = defaultdict(lambda: 0)
	for node in checkin_nodes:
		key = node[0] + "==>" + node[4]
		visit_count[key] += 1
	location_edges = []
	for key in visit2_count.keys():
		node_ids = key.split("==>")
		location_edges.append({"source": person_id_map[node_ids[0]],
							   "destination": location_map[node_ids[1]],
							   "visit_count": str(visit_count[key]),
							   "type": "visited"
							})
	print "Creating location edges"
	bulk_create_edges(location_edges)
	print

def main():
	checkin_nodes, location_map = create_location_nodes()
	utils.save_id_map(location_map,'location_id_map.txt')
	create_location_edges(checkin_nodes, location_map)
	print "DONE"
	print

if __name__ == "__main__":
	main()