#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py

#Modified by Jákup and Heidi 2022

# import the necessary packages
from flask import Flask, render_template, Response, request
from camera import VideoCamera

import serial
import time

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route("/control_master", methods=["POST"])
def control_master():
  value = request.form["value"]
  command = value
  # Do something with the value
  
  arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
  if command == "w":
      arduino.write(b'd')   # forward
      time.sleep(1)
  elif command == "a":
      arduino.write(b'a')   # left
      time.sleep(1)
  elif command == "d":
      arduino.write(b'd')   # rigt
      time.sleep(1)
  elif command == "s":  
      arduino.write(b's')   # backward
      time.sleep(1)
  elif command == "b":
      arduino.write(b'b')   # break
      time.sleep(1)
  elif command == "1":
      arduino.write(b'1')   # look down
      time.sleep(1)
  elif command == "2":
      arduino.write(b'2')   # look forward
      time.sleep(1)
  elif command == "3":
      arduino.write(b'3')   # look up
      time.sleep(1)
     
  # Send a response to the client
  serial.close() 
  return "You are now robo driving"
  
  
@app.route('/')
def watchdog():
    return render_template('watchdog.html') #you can customze .html here


def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')