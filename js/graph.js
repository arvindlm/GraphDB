

function main(){
	$("#graphStart").click(startClicked);
}

function startClicked(){
	var name = $("#graphInput").val().trim();
	if(name.length == 0){
		window.alert("Invalid input");
		return;
	}
	var req = {"first_name": name};
	var req = {"query": JSON.stringify(req)};
	api.getNode(req, loadGraph);
}

function loadGraph(response){
	$("#mainGraphPane").show();
	
	var width = $("#mainGraphPane").width();
	var height = $("#mainGraphPane").height();

	var force = d3.layout.force()
	    .size([width, height])
	    .nodes(response)
	    .linkDistance(function(x){return (Math.random() * 50)+50;})
	    .charge(-100)
	    .on("tick", tick);

	var svg = d3.select("#mainGraphPane").append("svg")
	    .attr("width", width)
	    .attr("height", height);

	svg.append("rect")
	    .attr("width", width)
	    .attr("height", height);

	var nodes = force.nodes(),
	    links = force.links(),
	    node = svg.selectAll(".node"),
	    link = svg.selectAll(".link");

	var div = d3.select("body").append("div")	
	    .attr("class", "tooltip alert alert-warning")				
	    .style("opacity", 0);

    restart();

	function nodeClick(selectedNode) {
		var point = d3.mouse(this);
		api.getNeighbours(selectedNode.zid, function(response){
			for(var i=0; i<response.length; i++){
				var addNodeFlag = true;
				for(var j=0; j<nodes.length; j++){
					if(response[i].zid === nodes[j].zid){
						addNodeFlag = false;
					}
				}
				if(addNodeFlag){
					response[i]['x'] = point[0];
					response[i]['y'] = point[1];
					nodes.push(response[i]);
				}
				var addLinkFlag = true;
				for(var j=0; j<links.length; j++){
					if(links[j].source.zid === selectedNode.zid && links[j].target.zid === response[i].zid){
						addLinkFlag = false;
					}
					if(links[j].source.zid === response[i].zid && links[j].target.zid === selectedNode.zid){
						addLinkFlag = false;
					}
				}
				if(addLinkFlag){
					links.push({source: selectedNode, target: response[i]});
				}
			}

			restart();
		});
	}

	function nodeHover(d) {
	  	node.transition()
	  		.duration(100)
			.attr('r', function(l) {
			    if (d.zid === l.zid)
			      return 20;
			    else
			      return 10;
			});

		div.transition()		
			.duration(100)		
			.style("opacity", 1);

		var disp = jQuery.extend({}, d);
		delete disp.index;
		delete disp.weight;
		delete disp.x;
		delete disp.y;
		delete disp.px;
		delete disp.py;
		delete disp.fixed;
		div.html(JSON.stringify(disp, null, 2))	
			.style("left", "10px")		
			.style("top", "60px");
	};

	function nodeMouseout() {
		node.transition()
			.duration(100)
			.attr('r', 10);
		div.transition()		
			.duration(100)		
			.style("opacity", 0);
	};

	function edgeHover(d) {
	  	link.transition()
	  		.duration(100)
			.attr('class', function(l) {
			    if (d.source.zid === l.source.zid && d.target.zid === l.target.zid){
			    	return "link highlight";
			    }
			    if (d.source.zid === l.target.zid && d.target.zid === l.source.zid){
			    	return "link highlight";
			    }
			    return "link";
			});

		div.transition()		
			.duration(100)		
			.style("opacity", 1);
		api.getEdge(d.source.zid, d.target.zid, function(response){
			div.html(JSON.stringify(response[0], null, 2))	
				.style("left", "10px")		
				.style("top", "60px");
		});
	};

	function edgeMouseout() {
		link.transition()
			.duration(100)
			.attr('class', 'link');
		div.transition()		
			.duration(100)		
			.style("opacity", 0);
	};

	function tick() {
		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });

		node.attr("cx", function(d) { return d.x; })
	    	.attr("cy", function(d) { return d.y; });
	}

	function restart() {
		link = link.data(links);

		link.enter().insert("line", ".node")
	    	.attr("class", "link")
	    	.on("mouseover", edgeHover)
	    	.on("mouseout", edgeMouseout);

		node = node.data(nodes);

		node.enter().insert("circle", ".cursor")
	    	.attr("class", function(n){return "node "+n.type;})
	    	.attr("r", 10)
	    	.on("click", nodeClick)
	    	.on("mouseover", nodeHover)
	    	.on("mouseout", nodeMouseout)
	    	.call(force.drag);

		force.start();
	}
}

//Calls function on page load
$(main);