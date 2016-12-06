import sys
from time import time
import zeusdb

PATH = "graph_data/"
person_id = {}

def tsv2list(path):
	#data = open(path, "r").read()
	X = []
	with open(path) as infile:
		for line in infile:
			X.append(line.rstrip('\r').rstrip('\n').split("\t"))
	return X
	#return [[x for x in line.rstrip("\r").split("\t")] for line in data.rstrip("\n").split("\n")]

def bulk_create_nodes(nodes, id_field):
	id_map = {}
	total = len(nodes)
	i = 1
	start_time = time()
	for node in nodes:
		new_id = zeusdb.create_node(node)
		sys.stdout.write("\rCreated "+str(i)+" nodes out of "+str(total)+" nodes")
		sys.stdout.flush()
		id_map[node[id_field]] = str(new_id)
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
		#print edge
		zeusdb.create_edge(edge)
		sys.stdout.write("\rCreated "+str(i)+" edges out of "+str(total)+" edges")
		sys.stdout.flush()
		i += 1
	end_time = time()
	print
	print "It took " + str(end_time-start_time) + " seconds to create " + str(total) + " edges"

def read_id_map(filename):
	id_map = {}
	with open(filename) as infile:
		for line in infile:
			key = line.rstrip('\n').rstrip('\r').split(' ')[0]
			val = line.rstrip('\n').rstrip('\r').split(' ')[1]
			id_map[key] = val
	return id_map

def save_id_map(id_map, filename):
	file = open(filename,'w')
	file.write('\n'.join(['%s %s'%(str(i),str(id_map[i])) for i in id_map]))
	file.close()
