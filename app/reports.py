from app import app, db, models
from flask import send_file

#######################################################################
# Reports v1.0 - Basic implementation of reports
#######################################################################

# Report all readings for sensor in .csv format
@app.route('/reports/<int:sensor_id>')
def testReport(sensor_id):
    file_name = app.root_path + "/tmp/report.csv"
    f = open(file_name, 'w')
    s = models.Sensor.query.get(sensor_id)
    if not s:
        abort (404)
    readings = s.readings.all()
    if not readings:
        abort (404)    
    for r in readings:
        f.write(str(r.TimeStamp)+",")
        f.write(str(r.Temperature)+",")
        f.write(str(r.Humidity))        
        f.write('\n')
    f.close()
    return send_file(file_name, as_attachment=True)

