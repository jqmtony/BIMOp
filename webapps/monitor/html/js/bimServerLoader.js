function getCreditialsFromBIMServer(address, username, password, target) {
	var client = new BimServerClient(address);
	client.init(function(){
		client.login(username, password, function(){
			client.call("ServiceInterface", "getAllProjects", {
					onlyTopLevel: true,
					onlyActive: true
				}, function(projects){
					var totalFound = 0;
					projects.forEach(function(project){
						if (project.lastRevisionId != -1) {
							var li = document.createElement("li");
							var a = document.createElement("a");
							li.appendChild(a);
							a.textContent = project.name;
							a.setAttribute("href", "docs/example_BIMServer.html?address=" + encodeURIComponent(address) + "&token=" + client.token + "&poid=" + project.oid + "&roid=" + project.lastRevisionId);
							ul.appendChild(li);
							totalFound++;
						}
					});
					if (totalFound == 0) {
						status.textContent = "No projects with revisions found on this server";
					} else {
						status.textContent = "";
					}
				});
			}, function(error){
				console.error(error);
				status.textContent = error.message;
			});
		});
	}
	
	loadFromBimserver("http://localhost:8082", "bimsurfer@logic-labs.nl", "bimsurfer", document.getElementById("expserver"));
	loadFromBimserver("http://localhost:8080", "admin@bimserver.org", "admin", document.getElementById("localhost8080"));
	loadFromBimserver("http://localhost:8082", "admin@bimserver.org", "admin", document.getElementById("localhost8082"));
	
	var loadLink = document.getElementById("loadFromOtherBimServer");
	loadLink.onclick = function(){
		document.getElementById("other").style.display = "block";
		if (localStorage.getItem("address") != null) {
			document.getElementById("address").value = localStorage.getItem("address");
			document.getElementById("username").value = localStorage.getItem("username");
			document.getElementById("password").value = localStorage.getItem("password");
		}
		document.getElementById("address").focus();
	};
	
	var loadProjectsBtn = document.getElementById("loadProjectsBtn");
	loadProjectsBtn.onclick = function(){
		var address = document.getElementById("address").value;
		var username = document.getElementById("username").value;
		var password = document.getElementById("password").value;
		localStorage.setItem("address", address);
		localStorage.setItem("username", username);
		localStorage.setItem("password", password);
		loadFromBimserver(address, username, password, document.getElementById("otherProjects"));
	};