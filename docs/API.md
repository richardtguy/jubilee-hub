# API v1.0
####Get list of registered sensors
|||
|---|---|
|URL:|`/api/v1.0/sensors/`|
|Method:|`GET`|
|Description:|Returns list of all registered sensors in JSON format|
|Example response:|`{  "sensors": [    {      "id": 2,      "interval": null,      "last_reading": "Mon, 18 Apr 2016 18:34:40 GMT",      "location": "somewhere",      "serial": "124",      "type": "any"    }  ]  }`|

####Get all readings for sensor
|||
|---|---|
|URL:|`/api/v1.0/sensors/<sensor_id>/readings`|
|Method:|`GET`|
|Description:|Returns list of all readings for selected sensor.|
|Example response:|`{  "readings": [    {      "humidity": null,       "temp": 999.9,       "timestamp": "Mon, 18 Apr 2016 15:12:27 GMT"    },     {      "humidity": null,       "temp": 9.9,       "timestamp": "Mon, 18 Apr 2016 15:16:59 GMT"    },  ] }`|

####Get latest reading
|||
|---|---|
|URL:|`/api/v1.0/sensors/<sensor_id>/readings/last`|
|Method:|`GET`|
|Description:|Returns most recent reading for selected sensor.|
|Example response:|`{  "last_reading": {    "humidity": null,     "temp": 69,     "timestamp": "Mon, 18 Apr 2016 18:02:08 GMT"  } }`|

####Get sensor settings
|||
|---|---|
|URL:|`/api/v1.0/sensors/<sensor_id>/settings`|
|Method:|`GET`|
|Description:|Returns settings information in JSON format for sensor with given ID.|
|Example response:|`{ "interval": null,   "last_reading": "Mon, 18 Apr 2016 18:02:08 GMT",   "location": "somewhere",   "serial": "124",   "type": "any" }`|

####Update sensor settings
|||
|---|---|
|URL:|`/api/v1.0/sensors/<sensor_id>/settings?key=xxxxxxxx`|
|Method:|`PUT`|
|Description:|Update sensor settings (location and interval between measurements)|
|Parameters:|`{ "interval": 123, "location": "somewhere" }`|
|Example response:|`{ "interval": null,   "last_reading": "Mon, 18 Apr 2016 18:02:08 GMT",   "location": "somewhere",   "serial": "124",   "type": "any" }`|

###Add reading
|||
|---|---|
|URL:|`/api/v1.0/sensors/<sensor_id>?key=xxxxxxxx`|
|Method:|`PUT`|
|Description:|Adds sensor reading(s), after checking correct has been sent as argument. Temperature, humidity or both. Updates date/time of last reading for sensor.|
|Parameters:|`{ "temp": 123 , "humidity": 123 }`|
|Example response:|`{  "success": "Sensor reading logged" }`|

###Register new sensor
|||
|---|---|
|URL:|`/api/v1.0/sensors?key=xxxxxxxx`|
|Method:|`POST`| 
|Parameters:|`{ "type":"any", "serial":"123", "location":"lounge" }`|
|Description:|Adds new sensor to table of registered sensors. Returns ID for new sensor, which must be identical to ID hardcoded in corresponding sensor.
|Example response:|`{  "success": "Sensor added",  "sensor_id": id }`|

###Delete sensor
|||
|---|---|
|URL:|`/api/v1.0/sensors/<sensor_id>`
|Method:|`DELETE`|
|Description:|Delete sensor and all corresponding readings.
|Example response:|`{  "success": "Sensor deleted" }`|
