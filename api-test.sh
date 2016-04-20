#!/bin/bash
#######################################################################
# API & Reporting test script
#######################################################################

echo "Testing jubilee API"

# Set IP address, port and host for development or production server
if [[ $1 == "--dev" ]]
then
	echo "Testing development server on localhost:5000"
	IP="localhost:5000"
	HOST="localhost"
elif [[ $1 == "--prod" ]]
then
	echo "Testing production server on jubilee-hub.local"
	IP="jubilee-hub.local"
else
	echo "[ERROR]  : Please select development (--dev) or production (--prod) server"
	exit
fi



# Register new sensor
test=$(curl --silent -i -H "Content-Type: application/json Host:"$HOST -X POST -d '{"type":"any", "serial":"123", "location":"somewhere"}' http://$IP/api/v1.0/sensors?key=6ABC61D3E5C546AEF558AF34E1E92)
if [[ $test =~ "success" ]] && [[ $test =~ "200" ]]
then
	echo "[OK]     : Registering new sensor"	
else
	echo "[FAILED] : Registering new sensor"
fi

# Log sensor reading
test=$(curl --silent -i -H "Content-Type: application/json" -X PUT -d '{"temp":999.9}' http://$IP/api/v1.0/sensors/1?key=6ABC61D3E5C546AEF558AF34E1E92)
if [[ $test =~ "success" ]] && [[ $test =~ "200" ]]
then
	echo "[OK]     : Logging new sensor reading"	
else
	echo "[FAILED] : Logging new sensor reading"
fi

# Get all readings for sensor
test=$(curl --silent -i http://$IP/api/v1.0/sensors/1/readings)
if [[ $test =~ "readings" ]] && [[ $test =~ "200" ]]
then
	echo "[OK]     : Getting all readings from sensor"	
else
	echo "[FAILED] : Getting all readings from sensor"
fi

# Get last reading from sensor and compare with test input
test=$(curl --silent -i http://$IP/api/v1.0/sensors/1/readings/last)
if [[ $test =~ "999.9" ]] && [[ $test =~ "200" ]]
then
	echo "[OK]     : Getting last reading from sensor"	
else
	echo "[FAILED] : Getting last reading from sensor"
fi

# Get list of sensors
test=$(curl --silent -i http://$IP/api/v1.0/sensors)
if [[ $test =~ "sensors" ]] && [[ $test =~ "200" ]]
then
	echo "[OK]     : Getting list of all registered sensors"	
else
	echo "[FAILED] : Getting list of all registered sensors"
fi

# Create report of all readings
if [ -f app/tmp/report.csv ]
then
	echo "[WARNING]: Report already exists, unable to test"
else
	test=$(curl --silent -i http://$IP/reports/1)
	if [ -f app/tmp/report.csv ]
	then
		echo "[OK]     : Writing report to report.csv"
	else
		echo "[FAILED] : Writing report"
	fi
fi

# Delete sensor
test=$(curl --silent -i -X DELETE http://$IP/api/v1.0/sensors/1?key=6ABC61D3E5C546AEF558AF34E1E92)
if [[ $test =~ "success" ]] && [[ $test =~ "200" ]]
then
	echo "[OK]     : Deleting sensor"	
else
	echo "[FAILED] : Deleting sensor"
fi


