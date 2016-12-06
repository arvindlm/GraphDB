from utils import read_id_map, tsv2list, PATH
from collections import defaultdict
import json

OUTPUT_FILE = 'checkin_edges.txt'

location_map = read_id_map('location_id_map.txt')
print "Processing location edges data"
person_id_map = read_id_map('person_id_map.txt')
visit_count = defaultdict(lambda: 0)

with open(PATH+"checkins.txt") as infile:
	for line in infile:
		node = (line.rstrip('\r').rstrip('\n').split("\t"))
		if node[0] == '' or node[4] =='':
			continue
		key = node[0] + "==>" + node[4]
		visit_count[key] += 1

print 'Done computing visitation count'
location_edges = []
for key in visit_count.keys():
	node_ids = key.split("==>")
	location_edges.append({"source": person_id_map[node_ids[0]],
						   "destination": location_map[node_ids[1]],
						   "visit_count": str(visit_count[key]),
						   "type": "visited"
						})

print 'Done making edges. Writing to file...'
with open(OUTPUT_FILE, 'w') as outfile:
	for edge in location_edges:
		outfile.write(json.dumps(edge))
		outfile.write('\n')

