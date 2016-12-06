import utils

def create_location_nodes():
	print
	print "Reading checkin nodes data file"
	checkin_nodes = utils.tsv2list(utils.PATH+"checkins.txt")
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
	location_map = utils.bulk_create_nodes(location_nodes, "location_id")
	return checkin_nodes, location_map

def main():
	checkin_nodes, location_map = create_location_nodes()
	utils.save_id_map(location_map,'location_id_map.txt')
	# location_map = utils.read_id_map('location_id_map.txt')
	# checkin_nodes  = utils.tsv2list(utils.PATH+"checkins.txt")

	# create_location_edges(checkin_nodes, location_map)
	print "DONE"
	print

if __name__ == "__main__":
	main()
