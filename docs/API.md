# API
||Get list of registered sensors|
|---|---|
|URL:|`/api/v1.0/sensors/`|
|Method:|`GET`|
|Description:|Returns list of all registered sensors in JSON format|
###Example response:
{
  "sensors": [
    {
      "id": 2,
      "interval": null,
      "last_reading": "Mon, 18 Apr 2016 18:34:40 GMT",
      "location": "somewhere",
      "serial": "124",
      "type": "any"
    }
  ]
}


URL: /api/v1.0/sensors/<sensor_id>/readings
METHOD: GET
DESCRIPTION: Returns list of all readings for selected sensor.
Example response: 
{
  "readings": [
    {
      "humidity": null, 
      "temp": 999.9, 
      "timestamp": "Mon, 18 Apr 2016 15:12:27 GMT"
    }, 
    {
      "humidity": null, 
      "temp": 9.9, 
      "timestamp": "Mon, 18 Apr 2016 15:16:59 GMT"
    }, 
  ]
}

URL: /api/v1.0/sensors/<sensor_id>/readings/last
METHOD: GET
DESCRIPTION: Returns most recent reading for selected sensor.
Example response: 
{
  "last_reading": {
    "humidity": null, 
    "temp": 69, 
    "timestamp": "Mon, 18 Apr 2016 18:02:08 GMT"
  }
}

URL: /api/v1.0/sensors/<sensor_id>/settings
METHOD: GET
DESCRIPTION: Returns settings information in JSON format for sensor with given ID.
{
  "interval": null, 
  "last_reading": "Mon, 18 Apr 2016 18:02:08 GMT", 
  "location": "somewhere", 
  "serial": "124", 
  "type": "any"
}

URL: /api/v1.0/sensors/<sensor_id>/settings?key=xxxxxxxx
METHOD: PUT
DESCRIPTION: Update sensor settings (location and interval between measurements)
USAGE: { "interval": 123, "location": "somewhere" }
Example response:
{
  "interval": null, 
  "last_reading": "Mon, 18 Apr 2016 18:02:08 GMT", 
  "location": "somewhere", 
  "serial": "124", 
  "type": "any"
}

URL: /api/v1.0/sensors/<sensor_id>?key=xxxxxxxx
METHOD: PUT
DESCRIPTION: Adds sensor reading(s), after checking correct has been sent as argument. Temperature,
humidity or both.
Updates date/time of last reading for sensor.
USAGE: { "temp": 123 , "humidity": 123 }
Example response:
{
  "success": "Sensor reading logged"
}

URL: /api/v1.0/sensors?key=xxxxxxxx
METHOD: POST 
USAGE: {"type":"any", "serial":"123", "location":"lounge"}
DESCRIPTION: Adds new sensor to table of registered sensors. Returns ID for new sensor, which must
be identical to ID hardcoded in corresponding sensor.
Example response:
{
  "success": "Sensor added",
  "sensor_id": id
}

URL: /api/v1.0/sensors/<sensor_id>
METHOD: DELETE
DESCRIPTION: Delete sensor and all corresponding readings.
EXAMPLE RESPONSE:
{
  "success": "Sensor deleted"
}

Tables for data logging server:

Sensors
  SensorID,
  Nickname,
  Sensor Type (will specify which values the sensor is expected to send),
  Date and time of last reading (DATETIME),
  Interval (time in s between readings)

Readings
  Date/time,
  SensorID,
  Temperature,
  Humidity

Variables hardcoded into sensor (to-do: store in EEPROM)
  key
  ID

When a sensor wakes up, it connects to the WLAN, sends a PUT statement with the latest sensor readings to the hub's IP address, then sends a GET statement to check if any settings need updating and updates itself e.g. sleep interval accordingly.