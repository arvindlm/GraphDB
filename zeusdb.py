import uuid
from cassandra.cluster import Cluster


KEYSPACE = "sample"
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
cluster = Cluster()
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
	props["node_id"] = uuid.UUID(props["source"])
	del props["source"]
	if "destination" not in props.keys():
		print "ERROR: No destination node id specified. Use key destination in props"
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
		res.extend(get_node_by_id(dest))
	return res