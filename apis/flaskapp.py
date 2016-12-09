from flask import Flask, jsonify, request
from flask.ext.cors import CORS
import zeusdb as zdb

app = Flask(__name__)
CORS(app)

@app.route('/info',methods=['GET'])
def get_info():
	data = zdb.get_info()
	return jsonify({"data": data, "success": True})

@app.route('/node/<node_id>',methods=['GET'])
def get_node_by_id(node_id):
	data = zdb.get_node_by_id(node_id)
	return jsonify({"data": data, "success": True})

@app.route('/node',methods=['POST'])
def create_node():
	#converting json string todictionary
	props = eval(request.json['data'])
	print props
	zid = zdb.create_node(props)
	props['zid'] = zid
	return jsonify({"data": props, "success": True})

@app.route('/edge',methods=['POST'])
def create_edge():
	props = request.json
	zid = zdb.create_edge(props)
	props['zid'] = zid
	return jsonify({"data": props, "success": True})

@app.route('/node/<node_id>/neighbour',methods=['GET'])
def get_neighbours(node_id):
	data = zdb.get_neighbours(node_id)
	return jsonify({"data": data, "success": True})

@app.route('/edge/<source_id>/<destination_id>',methods=['GET'])
def get_edge_between_nodes(source_id,destination_id):
	data = zdb.get_edge_between_nodes(source_id,destination_id)
	return jsonify({"data": data, "success": True})

@app.route('/edge/<edge_id>/<node_id>',methods=['DELETE'])
def delete_edge(edge_id,node_id):
	data = zdb.delete_edge(edge_id,node_id)
	return jsonify({"data": data, "success": True})

@app.route('/node/<node_id>',methods=['DELETE'])
def delete_node(node_id):
	data = zdb.delete_node(node_id)
	return jsonify({"data": data, "success": True})

if __name__ == '__main__':
	app.run(debug=True)
