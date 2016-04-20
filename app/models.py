# this module sets up classes to represent the database structure including tables
# for sensors and readings
# (for details of database design see docs/db_design.xml)

from app import db

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Serial = db.Column(db.String(64), unique=True)
    Type = db.Column(db.String(64))
    Location = db.Column(db.String(64))
    LastReading = db.Column(db.DateTime)
    Interval = db.Column(db.Integer)
    readings = db.relationship('Reading', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return '<Sensor %r %r %r>' % (self.id, self.Location, self.Serial)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TimeStamp = db.Column(db.DateTime)
    Sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    Temperature = db.Column(db.Integer)
    Humidity = db.Column(db.Integer)
    
    def __repr__(self):
        return "<Reading %r %r %r %r %r>" % (self.id, self.TimeStamp, self.Sensor_id, self.Temperature, self.Humidity)