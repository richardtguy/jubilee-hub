from app import app
from flask import render_template

@app.route('/lights')
def lights():
    return render_template('lights.html')

@app.route('/sensors')
def sensors():
    return render_template('sensors.html')
    
@app.route('/simple')
def simple():
    return render_template('simple.html')
