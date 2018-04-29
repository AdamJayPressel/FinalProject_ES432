#!/usr/bin/python
import random, json, requests, serial
from flask import (Flask,
                   request,
                   url_for,
                   render_template)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/data.json")
def data():
    # read temperature and humidity from Arduino
    s = serial.Serial("/dev/ttyACM0", 9600)

    s.write('p')
    
    dataStream = s.readline()
    
    splitData = dataStream.strip().split(',')
    indoor_temp = splitData[1]
    indoor_humidity = splitData[0]
            
    # read temperature and humidity from openweathermap.org
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?id=4347242&units=imperial&APPID=82e23dff4157ebabffea65f0497b0a81")
    data = r.json()
    outdoor_temp = data['main']['temp']
    outdoor_humidity = data['main']['humidity']
    
    # send the result as JSON
    return json.dumps({
        "indoor_temp": indoor_temp,
        "indoor_humidity": indoor_humidity,
        "outdoor_temp": outdoor_temp,
        "outdoor_humidity": outdoor_humidity})

#form, action is the url, and method post
@app.route("/cheep",methods=['POST'])
def cheep():
    s = serial.Serial("/dev/ttyACM0", 9600)

    name = request.form['name']
    message = request.form['message']
    
    with open("cheeps.log",'a') as f:
        f.write("%s: %s" % (name,message))
    # TODO: display the cheep on the kit LCD

    s.write('c')
    s.write(message.encode('utf-8'))
              
    return render_template('thankyou.html')



