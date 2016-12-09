

function main(){
	$.getJSON("/restConfig.json", loadPage);
}

function renderApi(log){
	var bgTerm = "success";
	if(log.type === "POST"){
		bgTerm = "warning";
	}
	else if(log.type === "DELETE"){
		bgTerm = "danger";
	}
	var iHtml = "<button class='btn btn-primary' id='"+log.id+"Try'>Try it!</button>";
	for(var i=log.params.length-1; i>=0; i--){
		iHtml = '<input class="form-control restInput" id="'+log.id+log.params[i]+'" placeholder="'+log.params[i]+'" />' + iHtml;
	}
	if(log.url.indexOf("[") != -1){
		var re = /\[(.*?)\]/g;
		var match;
		while(match = re.exec(log.url)){
			iHtml = '<input class="form-control restInput" id="'+log.id+match[1]+'" placeholder="'+match[1]+'" />' + iHtml;
		}
	}
	var res = ' \
		<div class="row restRow alert alert-'+bgTerm+'"> \
			<div class="btn-group"> \
				<button type="button" class="btn btn-'+bgTerm+' restBtn" data-toggle="collapse" data-target="#'+log.id+'Collapse" aria-expanded="false" aria-controls="'+log.id+'Collapse"> \
					'+log.type+' \
				</button> \
				<button type="button" class="btn btn-'+bgTerm+' restPathBtn" data-toggle="collapse" data-target="#'+log.id+'Collapse" aria-expanded="false" aria-controls="'+log.id+'Collapse"> \
					'+log.url+' \
				</button> \
			</div> \
			<div class="collapse" id="'+log.id+'Collapse"> \
			  <div class="well"> \
			    '+log.definition+' \
			  </div> \
			  '+iHtml+' \
			  <div class="well output" id="'+log.id+'Output"></div> \
			</div> \
		</div>';
	return res;
}

function bindLogEvents(log){
	$("#"+log.id+"Try").click(function(){
		var params = {};
		for(var i=0; i<log.params.length; i++){
			params[log.params[i]] = $("#"+log.id+log.params[i]).val();
		}

		var new_url = log.url;
		if(log.url.indexOf("[") != -1){
			var re = /\[(.*?)\]/g;
			var match;
			while(match = re.exec(log.url)){
				new_url = new_url.replace(match[0], $("#"+log.id+match[1]).val());
			}
		}
		
		var req_params = {
			"url": BASE_URL+new_url,
			"method": log.type,
			"data": params
		};
		if(log.type == "POST"){
			req_params["data"] = JSON.stringify(req_params["data"]);
			req_params["dataType"] = "json";
			req_params["contentType"] = "application/json";
		}
		$.ajax(req_params).done(function(data){
			if(typeof data === "string"){
				data = JSON.parse(data);
			}
			$("#"+log.id+"Output").html(JSON.stringify(data, null, 2));
		}).fail(function(){
			$("#"+log.id+"Output").html("Error in request");
		});
	});
}

function loadPage(config){
	for(var i=0; i<config.length; i++){
		config[i]['id'] = "restNode"+i;
		$("#restContainer").append(renderApi(config[i]));
		bindLogEvents(config[i]);
	}
}


//Calls function on page load
$(main);
