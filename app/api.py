from app import app, db, models
from flask import abort, make_response, jsonify, request
import datetime
from config import KEY

#######################################################################
# API v1.0 - Basic implementation of API, with minimal error checking
#######################################################################

# Get list of all registered sensors
# Usage: curl -i http://localhost:5000/api/v1.0/sensors
@app.route('/api/v1.0/sensors', methods=['GET'])
def get_sensors():
    sensors = models.Sensor.query.all()
    out = []
    for s in sensors:
        sensor = {
            'id': s.id,
            'serial': s.Serial,
            'type': s.Type,
            'last_reading': s.LastReading,
            'interval': s.Interval,
            'location': s.Location
        }
        out.append(sensor)
    return make_response(jsonify({'sensors': out}), 200)    

# Get list of all readings for a sensor
# Usage: curl -i http://localhost:5000/api/v1.0/sensors/1/readings
@app.route('/api/v1.0/sensors/<int:sensor_id>/readings', methods=['GET'])
def get_readings(sensor_id):
    s = models.Sensor.query.get(sensor_id)
    readings = s.readings.all()
    out = []
    for r in readings:
        reading = {
            'timestamp': r.TimeStamp,
            'temp': r.Temperature,
            'humidity': r.Humidity
        }
        out.append(reading)
    return make_response(jsonify({'readings': out}), 200)    

# Get most recent reading for a sensor
@app.route('/api/v1.0/sensors/<int:sensor_id>/readings/last', methods=['GET'])
def get_last_readings(sensor_id):
    s = models.Sensor.query.get(sensor_id)
    readings = s.readings.all()
    last = models.Reading.query.filter_by(TimeStamp=s.LastReading).first()
    reading = {
        'timestamp': last.TimeStamp,
        'temp': last.Temperature,
        'humidity': last.Humidity
    }
    return make_response(jsonify({'last_reading': reading}), 200)    

# Get settings for a sensor
# Usage: curl -i http://localhost:5000/api/v1.0/sensors/1/settings
@app.route('/api/v1.0/sensors/<int:sensor_id>/settings', methods=['GET'])
def get_sensor(sensor_id):
    s = models.Sensor.query.get(sensor_id)
    return make_response(jsonify({'serial': s.Serial, 'type': s.Type, 
        'last_reading': s.LastReading, 'location': s.Location,
        'interval': s.Interval}), 200)    

# Update settings for a sensor
# Usage: 
@app.route('/api/v1.0/sensors/<int:sensor_id>/settings', methods=['PUT'])
def update_settings(sensor_id):
    if request.args.get('key', '') != KEY:
        abort(403)
    s = models.Sensor.query.get(sensor_id)
    s.Interval = request.json.get('interval')
    s.Location = request.json.get('location')
    db.session.add(s)
    db.session.commit()
    return make_response(jsonify({'serial': s.Serial, 'type': s.Type, 
        'last_reading': s.LastReading, 'location': s.Location,
        'interval': s.Interval}), 200)    

# Register new sensor
# Usage: curl -i -H "Content-Type: application/json" -X POST -d '{"type":"any", 
# "serial":"123", "location":"lounge"}' http://localhost:5000/api/v1.0/sensors?
# key=ABC 
# Sensor serial number must be unique, all arguments must be included.
@app.route('/api/v1.0/sensors', methods=['POST'])
def register_sensor():
    if request.args.get('key', '') != KEY:
        abort(403)
    new_sensor = models.Sensor(Serial=request.json['serial'], 
        Type=request.json['type'], Location=request.json['location'])
    db.session.add(new_sensor)
    db.session.commit()
    id = new_sensor.id    
    return make_response(jsonify({'success': 'Sensor added', 'sensor_id': id}),
        200)    

# Delete sensor and all associated readings
# Usage: curl -i -X DELETE http://localhost:5000/api/v1.0/sensors/1?key=ABC
@app.route('/api/v1.0/sensors/<int:sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    if request.args.get('key', '') != KEY:
        abort(403)  
    s = models.Sensor.query.get(sensor_id)    
    r = s.readings.all()
    for i in r:
        db.session.delete(i)
    db.session.delete(s)
    db.session.commit()
    return make_response(jsonify({'success': 'Sensor deleted'}), 200)    
    
# Add a new sensor reading
# Usage: curl -i -H "Content-Type: application/json" -X PUT -d '{"temp":23.2}' 
# http://localhost:5000/api/v1.0/sensors/1?key=ABC
@app.route('/api/v1.0/sensors/<int:sensor_id>', methods=['PUT'])
def put_reading(sensor_id):
    if request.args.get('key', '') != KEY:
        abort(403)
    s = models.Sensor.query.get(sensor_id)
    if not s:
        abort(404)
    t = request.json.get('temp')
    h = request.json.get('humidity')
    now = datetime.datetime.utcnow()
    r = models.Reading(TimeStamp=now, Temperature=t, Humidity=h, author=s)
    db.session.add(r)
    s.LastReading = now
    db.session.add(s)
    db.session.commit()
    return make_response(jsonify({'success': 'Sensor reading logged'}), 200)

@app.errorhandler(501)
def no_service(error):
    return make_response(jsonify({'error': 'Service not implemented'}), 501)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)
    
@app.errorhandler(403)
def wrong_key(error):
    return make_response(jsonify({'error': 'Incorrect key'}), 403)
    
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
