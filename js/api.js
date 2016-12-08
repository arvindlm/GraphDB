BASE_URL = "http://ec2-54-187-92-200.us-west-2.compute.amazonaws.com";

INFO_URL = BASE_URL + "/info";
NODE_URL = BASE_URL + "/node";
EDGE_URL = BASE_URL + "/edge";
QUERY_URL = "/query";
NEIGHBOUR_URL = "/neighbour";



function responseWrapper(response, callback){
	if(typeof response === "string"){
		response = JSON.parse(response);
	}
	if(response.success){
		callback(response.data);
	}
	else{
		alert("Something went wrong!");
	}
}

api = {
	getInfo: function(callback){
		$.get(INFO_URL, function(response){
			responseWrapper(response, callback);
		});
	},

	getNode: function(req, callback){
		$.get(NODE_URL+QUERY_URL, req, function(response){
			responseWrapper(response, callback);
		});
	},

	getNeighbours: function(_id, callback){
		$.get(NODE_URL+"/"+_id+NEIGHBOUR_URL, function(response){
			responseWrapper(response, callback);
		});
	},

	getEdge: function(source, target, callback){
		$.get(EDGE_URL+"/"+source+"/"+target, function(response){
			responseWrapper(response, callback);
		});
	},
}
