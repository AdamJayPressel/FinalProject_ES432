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
    s = Serial.serial('/dev/ttyAMC0')
    s.write('p')
    dataStream = s.readline()
    if(dataStream is None or dataStream==''):
        #TODO
        pass
    splitData = dataStream.rstrip().split(',')
    indoor_temp = splitData[1]
    indoor_humidity = splitData[0]
    s.close()
    
    # read temperature and humidity from openweathermap.org
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?id=4347242&units=imperial&APPID=82e23dff4157ebabffea65f0497b0a81"
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
    name = request.form['name']
    message = request.form['message']
    print("got a cheep from [%s]: %s" % (name,message))
    # TODO: append [name: message] to a file of cheeps
    with open("cheeps.log",'a') as f:
                     f.write("%s, %s" %(name,messge))
    # TODO: display the cheep on the kit LCD
                     
    return render_template('thankyou.html')



