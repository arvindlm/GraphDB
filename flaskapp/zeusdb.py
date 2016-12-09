import uuid
from cassandra.cluster import Cluster
import index

KEYSPACE = "zeus"
NODE_TABLE = "node"
EDGE_TABLE = "edge"

# By default, takes localhost
# For actual, specify all the machine ip as a list
# cluster = Cluster(['192.168.0.1', '192.168.0.2'])
# The set of IP addresses we pass to the Cluster is
# simply an initial set of contact points. After the
# driver connects to one of these nodes it will
# automatically discover the rest of the nodes in the
# cluster and connect to them, so you don't need to
# list every node in your cluster.
print "Connecting with the cassandra cluster"
cluster = Cluster(['54.218.56.39'])
session = cluster.connect(KEYSPACE)
print "Connected"
print

def get_uuid():
	return uuid.uuid1()

def get_column_names(table):
	rows = session.execute(
		"""
			SELECT column_name FROM system_schema.columns
			WHERE table_name=%s AND keyspace_name=%s;
		""",
		(table, KEYSPACE)
	)
	return [row.column_name for row in rows]

def create_column(column, table):
	query = "ALTER TABLE " + table + " ADD " + column + " varchar;"
	session.execute(query)

def check_and_create_columns(columns, table):
	existing_columns = get_column_names(table)
	for column in columns:
		if column not in existing_columns:
			create_column(column, table)

def insert_props(props, table):
	query = "INSERT INTO " + table + " ("
	for key in props.keys():
		query += key +", "
	query = query[:-2] + ") VALUES (" + ("%s, " * len(props))[:-2] + ")"
	session.execute(query, props.values())

def get_dict_from_row(row):
	fields = row._fields
	res = {}
	for field in fields:
		val = getattr(row, field)
		if val != None:
			res[field] = str(val)
	return res

# GET GRAPH INFO
def get_info():
	query = "SELECT COUNT(*) FROM " + NODE_TABLE
	num_nodes = session.execute(query)
	query = "SELECT COUNT(*) FROM " + EDGE_TABLE
	num_edges = session.execute(query)
	rslt = {"node": num_nodes,"edge":num_edges}
	return {"count": rslt}

# CREATE NODE
def create_node(props):
	props['zid'] = get_uuid()
	check_and_create_columns(props.keys(), NODE_TABLE)
	insert_props(props, NODE_TABLE)
	return props['zid']

# CREATE EDGE
def create_edge(props):
	if "source" not in props.keys():
		print "ERROR: No source node id specified. Use key source in props"
		return
	props["node_id"] = uuid.UUID(props["source"])
	del props["source"]
	if "destination" not in props.keys():
		print "ERROR: No destination node id specified. Use key destination in props"
		return
	props["destination"] = uuid.UUID(props["destination"])
	props["zid"] = get_uuid()
	check_and_create_columns(props.keys(), EDGE_TABLE)
	insert_props(props, EDGE_TABLE)
	return props["zid"]

# GET NODE BY ID
def get_node_by_id(_id):
	_id = uuid.UUID(_id)
	query = "SELECT * FROM " + NODE_TABLE + " WHERE zid=%s"
	rows = session.execute(query, (_id,))
	res = []
	for row in rows:
		res.append(get_dict_from_row(row))
	return res

# GET NEIGHBOURS
def get_neighbours(_id):
	_id = uuid.UUID(_id)
	query = "SELECT * FROM " + EDGE_TABLE + " WHERE node_id=%s"
	rows = session.execute(query, (_id,))
	destinations = [row.destination for row in rows]
	res = []
	for dest in destinations:
		res.extend(get_node_by_id(str(dest)))
	return res

#GET EDGE BY SOURCE AND DESTINATION
def get_edge_between_nodes(source_id,destination_id):
	_sid = uuid.UUID(source_id)
	_did = uuid.UUID(destination_id)
	query = "SELECT * FROM " + EDGE_TABLE + " WHERE node_id=%s AND destination=%s"
	rows = session.execute(query, (_sid,_did))
	res = []
	for row in rows:
		res.append(get_dict_from_row(row))
	return res

#DELETE EDGE BY ID AND NODE_ID
def delete_edge(_id,node_id):
	_id = uuid.UUID(_id)
	node_id = uuid.UUID(node_id)
	query = "DELETE FROM " + EDGE_TABLE + " WHERE zid=%s AND node_id=%s"
	#call for deleting edge in index table
	rows = session.execute(query, (_id,node_id))
	res = []
	for row in rows:
		res.append(get_dict_from_row(row))
	return res

def delete_node(_id):
	_id = uuid.UUID(_id)
	query = "SELECT * FROM " + EDGE_TABLE + " WHERE node_id=%s"
	rows = session.execute(query, (_id,))
	edges = []
	for row in rows:
		edges.append(get_dict_from_row(row))

	#deleting all edges linked to the node
	for edge in edges:
		zid = uuid.UUID(edge['zid'])
		query = "DELETE FROM " + EDGE_TABLE + " WHERE node_id=%s AND zid=%s"
		session.execute(query,(_id,zid))

	query = "DELETE FROM " + NODE_TABLE + " WHERE zid=%s"
	session.execute(query, (_id,))
	return

# GET NODE/EDGE BY PROPERTY
def get_object_by_property(table, properties):
        for prop in properties:
                if not index.is_field_indexed(table, prop):
                        print "Index not created for one or more properties"
                        return
        body = index.build_query_json(properties)
        items = index.search_all_indexes(table, body)
	res = []
        for item in items
		res.push(get_node_by_id(item)
	return res

def get_node_by_property(properties):
	return get_object_by_property(NODE_TABLE, properties)

def get_edge_by_property(properties):
	return get_object_by_property(EDGE_TABLE, properties)
