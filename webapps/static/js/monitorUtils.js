
function querySensorData(queryType, sensorType){
	$.get("sensorsDataQuery/" + queryType + "/" + sensorType, function(data, status){
        if (Object.keys(data.errors).length == 0){
        	nowTime = new Date();
        	queryResults = data.sensorsDataQuery.queryResults;
        	isQueryOutofdate = false; // At least one query result is not up to date
        	isQueryBad = false; // At least one query result is bad
        	for (var i=0; i<queryResults.length; i++){
        		queryResult = queryResults[i];
        		queryGuid = queryResult.guid;
        		thisSensorDataInfoDict = {};
        		thisSensorDataInfoDict['name'] = queryResult.name;
        		thisSensorDataInfoDict['value'] = parseFloat(queryResult.value).toFixed(2);
        		thisSensorDataInfoDict['unit'] = project_bim_components_info[queryGuid][displaySensorType];
        		thisSensorDataInfoDict['isGood'] = queryResult.isGood;
        		thisSensorDataInfoDict['notes'] = queryResult.notes;
        		thisSensorDataInfoDict['recordedTime'] = new Date(queryResult.recordedTime);   		
        		thisSensorDataInfoDict['queryTime'] = nowTime;
        		thisSensorDataInfoDict['isOutOfDate'] = false;
        		if (thisSensorDataInfoDict['isGood']){      			
        			if ((nowTime - thisSensorDataInfoDict['recordedTime']) > realTimeSyncToleranceInMS){
        				textVectorContent = "!!" + thisSensorDataInfoDict['value'] + thisSensorDataInfoDict['unit'];
        				textVectorEmissive = [1.0, 0.0, 0.0]
        				thisSensorDataInfoDict['isOutOfDate'] = true;
        				isQueryOutofdate = true;
        			}
        			else{
        				textVectorContent = "" + thisSensorDataInfoDict['value'] + thisSensorDataInfoDict['unit'];
        				textVectorEmissive = [0.0, 0.0, 0.0]
        			}
        		}
        		else{
        			textVectorContent = "??" + thisSensorDataInfoDict['unit'];
        			textVectorEmissive = [1.0, 0.0, 0.0]
        			isQueryBad = true;
        		}
        		thisRelatedEntityId = project_components_text_guidNEntityid[queryGuid];
        		scene.entities[thisRelatedEntityId].material.emissive = textVectorEmissive;
        		scene.entities[thisRelatedEntityId].geometry.text = textVectorContent;
        		components_sensorData_info_now[queryGuid] = thisSensorDataInfoDict;
        	}
        	addMsgToStatus("info", "Sensor data are updated")
        	addMsgToUpdateAt(nowTime)
        	if (isQueryOutofdate){
        		addMsgToStatus("warning", "At least one sensor data is out of date");
        	}
        	if (isQueryBad){
        		addMsgToStatus("warning", "At least one sensor data is in bad status")
        	}
        }
        else{
        	addMsgToStatus("warning", "Sensor data cannot be updated. Error message from server: " + data.errors)
        }
    });
}

function addMsgToUpdateAt(nowTime){
	document.getElementById("updatedAt").innerHTML = "Updated at " + nowTime
}

function addMsgToStatus(msgLevel, msg){
	newDiv = document.createElement("div");
	if (msgLevel == "warning"){
		newDiv.innerHTML = "[" + new Date + "] " + "WARNING:" + msg;
		newDiv.style.color = "Red";
	}
	else if (msgLevel == "info"){
		newDiv.innerHTML = "[" + new Date + "] " + "INFO:" + msg;
	}
	statusDiv = document.getElementById("status");
	statusDiv.appendChild(newDiv);
	if (statusDiv.childElementCount > maxStatusMsgNumber){
		statusDiv.removeChild(statusDiv.firstElementChild)
	}
}

function displaySensorData(currentSelectedGuid, dataContainerName, components_sensorData_info_now){
	thisSensorData = components_sensorData_info_now[currentSelectedGuid];
	container = document.getElementById(dataContainerName);
	container.innerHTML = "";
	guidDiv = document.createElement('div');
	guidDiv.innerHTML = 'GUID:' + currentSelectedGuid;
	container.appendChild(guidDiv);
	showNoteRed = false;
	if (thisSensorData != null){
		Object.keys(thisSensorData).forEach(function(key){
			thisDiv = document.createElement('div');
			if (key == "isGood" && thisSensorData[key] == false){
				thisDiv.style.color = "Red";
				showNoteRed = true;
			}
			if (key == "notes" && showNoteRed){
				thisDiv.style.color = "Red";
			}
			if (key == "isOutOfDate" && thisSensorData[key] == true){
				thisDiv.style.color = "Red";
				thisDiv.innerHTML = key + ":" + thisSensorData[key] + "(Sensor data is significantly behind the current time)";
			}
			else{
				thisDiv.innerHTML = key + ":" + thisSensorData[key]
			}
			container.appendChild(thisDiv);
		})
	}
	else{
		thisDiv = document.createElement('div');
		thisDiv.style.color = "Red";
		thisDiv.innerHTML = "The sensor data has not been set"
		container.appendChild(thisDiv);


	}
}

function clearDisplay(dataContainerName, defaultText){
	container = document.getElementById(dataContainerName);
	container.innerHTML = defaultText;
}


function openDataTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function displaySensorHist(currentSelectedGuid, sensorType, histLengthHours, divId){
	nowTime = new Date()
	nowTime2 = new Date()
	nowTime2.setHours(nowTime2.getHours() - histLengthHours);
	displaySensorHistUrl = "sensorsDataQuery/" + "histSingle" + "/" + sensorType + "/" + currentSelectedGuid + "/" 
		+ nowTime2.toISOString() + "/" + nowTime.toISOString();
	$.get(displaySensorHistUrl, function(data, status){
			if (Object.keys(data.errors).length == 0){
				dataForChart = [];
				queryResults = data.sensorsDataQuery.queryResults;
				for (var i=0; i<queryResults.length; i++){
					queryResult = queryResults[i];
					thisDataForChart = []
					recordedTimeDate = new Date(queryResult.recordedTime)
					thisDataForChart.push(recordedTimeDate.getTime())
					if (queryResult.isGood){
						thisDataForChart.push(parseFloat(queryResult.value))
					}else{
						thisDataForChart.push(parseFloat("0.0"))
					}
					dataForChart.push(thisDataForChart);
				}
				//Hight chart
				Highcharts.chart(divId, {
			        chart: {
			            zoomType: 'x'
			        },
			        title: {
			            text: 'Time-series sensor data'
			        },
			        xAxis: {
			            type: 'datetime'
			        },
			        yAxis: {
			            title: {
			                text: sensorType
			            }
			        },
			        legend: {
			            enabled: false
			        },
			        plotOptions: {
			            area: {
			                fillColor: {
			                    linearGradient: {
			                        x1: 0,
			                        y1: 0,
			                        x2: 0,
			                        y2: 1
			                    },
			                    stops: [
			                        [0, Highcharts.getOptions().colors[0]],
			                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
			                    ]
			                },
			                marker: {
			                    radius: 2
			                },
			                lineWidth: 1,
			                states: {
			                    hover: {
			                        lineWidth: 1
			                    }
			                },
			                threshold: null
			            }
			        },

			        series: [{
			            type: 'area',
			            name: currentSelectedGuid,
			            data: dataForChart
			        }]
    			});

				//document.getElementById(divId).innerHTML = JSON.stringify(dataForChart);
			}

			

		});
}