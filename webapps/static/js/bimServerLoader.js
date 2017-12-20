function getCreditialsFromBIMServer(address, username, password, tgtpoid) {
	var client = new BimServerClient(address);
	alert("here0")
	client.init(function(){
		alert("here01")
		client.login(username, password, function(){
			alert("here02")
			client.call("ServiceInterface", "getProjectByPoid", {
					poid: tgtpoid
				}, function(tgtproject){
					alert("here1")
						if (tgtproject.lastRevisionId != -1) {
							alert("here2")
							return {"token": client.token,
									"poid": project.oid,
									"roid": project.lastRevisionId};
						}
				});
			}, function(error){
				alert(error)

			});
		});
	}