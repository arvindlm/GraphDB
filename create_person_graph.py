import utils

def create_person_nodes():
	print
	print "Reading person nodes data file"
	person_nodes = utils.tsv2list(PATH+"personNodes.txt")
	person_nodes = [{"id": x[0],
					 "first_name": x[1],
					 "last_name": x[2],
					 "gender": x[3],
					 "age": x[4],
					 "type": "person"
					} for x in person_nodes]

	print "Creating person nodes"
	person_id_map = utils.bulk_create_nodes(person_nodes, "id")
	return person_id_map

def create_person_edges(person_id_map):
	print
	print "Reading person edges data file"
	person_edges = tsv2list(PATH+"personEdges.txt")
	person_edges = [{"source": person_id_map[x[0]],
					 "destination": person_id_map[x[1]],
					 "type": "friend"
					} for x in person_edges]
	print "Creating person edges"
	bulk_create_edges(person_edges)
	print

def main():
	person_id_map = create_person_nodes()
	utils.save_id_map(person_id_map,'person_id_map.txt')
	create_person_edges(person_id_map)
	print "DONE"
	print

if __name__ == "__main__":
	main()