from flask import Flask, jsonify, request
import zeusdb as zdb

app = Flask(__name__)

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
	props = request.json
	zid = zdb.create_node(props)
	props['zid'] = zid
	return jsonify({"data": props, "success": True})

@app.route('/edge',methods=['POST'])
def create_edge():
	props = request.json
	zid = zdb.create_edge(props)
	props['zid'] = zid
	return jsonify({"data": props, "success": True})

@app.route('/node/<node_id>/neighbours',methods=['GET'])
def get_neighbours(node_id):
	data = zdb.get_neighbours(node_id)
	return jsonify({"data": data, "success": True})

if __name__ == '__main__':
	app.run(debug=True)