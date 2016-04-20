/*
Really simple interface for Logger
- To-do: improve on minimal error handling
- Improve security by requiring user to submit KEY first time (then store in
  cookie)
*/

// Set IP address for logger (is there a way to pass this along with the JS?)
//Production server
var loggerIP = "jubilee-hub.local";
var port = "80"
//Dev server
//var loggerIP = "localhost";
//var port = "5000"

// Set KEY for API
var KEY = "6ABC61D3E5C546AEF558AF34E1E92";

// Get details of registered sensors and output to browser page in table
function initialise(IP, port) {
	// Write blank table for sensor details
	var html = "	<table id=\"sensors\">\
						<tr>\
							<th>ID</th>\
							<th>Serial</th>\
							<th>Type</th>\
							<th>Location</th>\
							<th>Last Read</th>\
							<th></th>\
						</tr>\
					</table>";
    document.getElementById("sensorTable").innerHTML = html;
    
    // Get details of registered sensors and write into table
	console.log('Attempting to contact Logger on IP: ' + IP + ', port: ' + port);
	var xmlhttp = new XMLHttpRequest();
	var url = "http://" + IP + ":" + port + "/api/v1.0/sensors";
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			console.log(xmlhttp.responseText);
			var response = JSON.parse(xmlhttp.responseText);
			console.log('Number of sensors = '+ response.sensors.length);
			var table = document.getElementById("sensors");
		    for (i=0; i<response.sensors.length; i++) {
		    	var row = table.insertRow(-1);
		    	var cell1 = row.insertCell(0);
		    	var cell2 = row.insertCell(1);
				var cell3 = row.insertCell(2);
				var cell4 = row.insertCell(3);
				var cell5 = row.insertCell(4);
				var cell6 = row.insertCell(5);
				cell1.innerHTML = response.sensors[i].id;
				cell2.innerHTML = response.sensors[i].serial;
				cell3.innerHTML = response.sensors[i].type;
				cell4.innerHTML = response.sensors[i].location;
				cell5.innerHTML = response.sensors[i].last_reading;
				cell6.innerHTML = "<i class=\"w3-btn\" \
					onclick=\"deleteSensor(loggerIP, port, "
					+response.sensors[i].id+")\">Delete</i>\
					<i class=\"w3-btn\" onclick=\"listReadings(loggerIP, port, "
					+response.sensors[i].id+")\">List</i>\
					<i class=\"w3-btn\" onclick=\"location.href='reports/"
					+response.sensors[i].id+"'\">Download</i>";
			}
		}
	}
	xmlhttp.open("GET", url, true);
	xmlhttp.ontimeout = function () {
		alert("Error! Unable to connect to server");
	}
	xmlhttp.send();
}

// Delete sensor
function deleteSensor(IP, port, sensor_id) {
	console.log('Deleting sensor: ' + sensor_id);
	var xmlhttp = new XMLHttpRequest();
	var url = "http://" + IP + ":" + port + "/api/v1.0/sensors/" + sensor_id + "?key=" + KEY;
 	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			console.log('Success');
			// Refresh sensor table
			initialise(IP, port);
		}
	}
	xmlhttp.open("DELETE", url, true);
	xmlhttp.ontimeout = function () {
		alert("Error! Unable to connect to server");
	}
	xmlhttp.send();
}

// List readings for sensor
function listReadings(IP, port, sensor_id) {
	console.log('Listing all readings for sensor: ' + sensor_id);
	var html = "<h2>Sensor: "+sensor_id+"</h2>\
		<table id=\"readings\" style=\"width:50%\">\
						<tr>\
							<th>Temp</th>\
							<th>Humidity</th>\
							<th>Time</th>\
							<th></th>\
						</tr>\
					</table>";
    document.getElementById("sensorReadings").innerHTML = html;
	var xmlhttp = new XMLHttpRequest();
	var url = "http://" + IP + ":" + port + "/api/v1.0/sensors/"+sensor_id+"/readings?key="+KEY;
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			console.log(xmlhttp.responseText);
			var response = JSON.parse(xmlhttp.responseText);
			console.log('Number of readings = '+ response.readings.length);
			var table = document.getElementById("readings");
		    for (i=0; i<response.readings.length; i++) {
		    	var row = table.insertRow(-1);
		    	var cell1 = row.insertCell(0);
		    	var cell2 = row.insertCell(1);
				var cell3 = row.insertCell(2);
				cell1.innerHTML = response.readings[i].temp;
				cell2.innerHTML = response.readings[i].humidity;
				cell3.innerHTML = response.readings[i].timestamp;		    	
			}
		}
	}
	xmlhttp.open("GET", url, true);
	xmlhttp.ontimeout = function () {
		alert("Error! Unable to connect to server");
	}
	xmlhttp.send();
}


// Add sensor
function addSensor(IP, port) {
	console.log('Adding new sensor...');
	
	var data = {};
	data.serial = document.getElementById("serial").value;
	data.type = document.getElementById("type").value;
	data.location = document.getElementById("location").value;
	
	var xmlhttp = new XMLHttpRequest();
	var url = "http://" + IP + ":" + port + "/api/v1.0/sensors?key="+KEY;
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			console.log('Success');
			// Refresh sensor table
			initialise(IP, port);
		}
	}
	xmlhttp.open("POST", url, true);
	xmlhttp.setRequestHeader("Content-type", "application/json");
	xmlhttp.ontimeout = function () {
		alert("Error! Unable to connect to server");
	}
	xmlhttp.send(JSON.stringify(data));
}

// Display last reading for sensor
function lastReading(IP, port, sensor_id) {
	console.log('Listing most recent reading for sensor: ' + sensor_id);
	var xmlhttp = new XMLHttpRequest();
	var url = "http://" + IP + ":" + port + "/api/v1.0/sensors/"+sensor_id+"/readings/last?key="+KEY;
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			var response = JSON.parse(xmlhttp.responseText);
			console.log(xmlhttp.responseText);
			document.getElementById("id01").innerHTML = response.last_reading.temp;
			document.getElementById("id02").innerHTML = response.last_reading.timestamp;
		}
	}
	xmlhttp.open("GET", url, true);
	xmlhttp.ontimeout = function () {
		alert("Error! Unable to connect to server");
	}
	xmlhttp.send();
}