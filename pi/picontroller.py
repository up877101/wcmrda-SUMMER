# Raspberry Pi server component for controlling robot, recieves
# input from the web server routes and passes commands onto 
# the AStar board via
import sys
import socket
import time
from imutils.video import VideoStream
import imagezmq
from flask import Flask
from multiprocessing import Process
from a_star import AStar

# note that: imageStreamer has a hardcoded IP for client, may
# need updating for demo purposes. IP and port has been redacted
# just for the purpose of uploading to a repository

a_star = AStar()
app = Flask(__name__)

# procedure that runs in a multiprocess node on start
def imageStreamer():
    sender = imagezmq.ImageSender(connect_to='tcp://IP:PORT')

    rpi_name = socket.gethostname() # send RPi hostname with each image
    picam = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)  # allow camera sensor to warm up
    while True:  # send images as stream until Ctrl-C
        image = picam.read()
        sender.send_image(rpi_name, image)

@app.route('/')
def base():
    return 'app running'

# managing drive speeds
@app.route('/driveForward')
def driveForward():
    a_star.write_motors('f', 30)

    return 'moving forward'

@app.route('/driveBackward')
def driveBackward():
    a_star.write_motors('b', 30)

    return 'moving backward'

@app.route('/driveStop')
def driveStop():
    a_star.write_motors('f', 0)

    return 'stopping drive'

# managing steer direction
@app.route('/steerNeutral')
def steerNeutral():
    a_star.write_steer(90)

    return 'resetting steer'

@app.route('/steerLeft')
def steerLeft():
    a_star.write_steer(5)

    return 'steering left'

@app.route('/steerRight')
def steerRight():
    a_star.write_steer(175)

    return 'steering right'

# managing the video stream
@app.route('/startVideo')
def startVideo():
    global streamer
    streamer = Process(target=imageStreamer)
    streamer.start()
    
    return 'started video'

@app.route('/stopVideo')
def stopVideo():
    streamer.terminate()

    return 'stopped video'

# starting the app
if __name__ == '__main__':
    app.run(debug=False, port=PORT, host='IP')