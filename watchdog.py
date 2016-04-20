#!flask/bin/python

from app import app, db, models
import datetime

#######################################################################
# Watchdog v1.0 - Basic implementation of watchdog
#######################################################################

# This module will run in the background, polling the database to compare sensor states
# against defined rules and taking actions accordingly.

# monitor temperature on sensor and warn if high
def checkRule(sensor_id, comparator, threshold):
    s = models.Sensor.query.get(sensor_id)
    if not s:
        return False
    last = models.Reading.query.filter_by(TimeStamp=s.LastReading).first()
    if comparator == "gt":
        if last.Temperature > threshold:
            now = datetime.datetime.utcnow()
            result = "NOTE! Temperature on sensor "+str(s.id)+" ("+str(last.Temperature)
            +") exceeds threshold ("+str(threshold)+") at "+str(now)
        else:
            result = False
    elif comparator == "lt":
        if last.Temperature < threshold:
   	        now = datetime.datetime.utcnow()
   	        result = "NOTE! Temperature on sensor "+str(s.id)+" ("+str(last.Temperature)
   	        +") below threshold ("+str(threshold)+") at "+str(now)
        else:
            result = False	
    return result


# Initialise log file
file_name = app.root_path + "/tmp/watchdog.log"
print "Starting watchdog..."
now = datetime.datetime.utcnow()
with open(file_name, 'a') as f:
    f.write("Starting watchdog at "+str(now)+"\n")

# Initialise rules
rule1 = False
rule2 = False

# Monitor sensors and write to log file when rule changes to true
while True:
    # Rule 1: If Sensor 1 temperature becomes greater than 100.0 
    before = rule1
    rule1 = checkRule(1, "gt", 100)
    if before == False and rule1 != False:
        print rule1
        with open(file_name, 'a') as f:
            f.write(rule1 + '\n')
        
    # Rule 2: If Sensor 2 temperature becomes less than 100.0 
    before = rule2
    rule2 = checkRule(2, "lt", 100)
    if before == False and rule2 != False:
        print rule2
        with open(file_name, 'a') as f:
            f.write(rule2 + '\n')