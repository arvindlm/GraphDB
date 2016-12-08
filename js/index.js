

function main(){
	api.getInfo(function(data){
		$("#node_count").html(data.count.node);
		$("#edge_count").html(data.count.edge);
	});
}



//Calls function on page load
$(main);