# Network controller class that serves to manage and group all functionality
# related to communication between the client application and the picontroller
# web server that runs on the Raspberry Pi.

import requests
import imagezmq

# note that: Pi's IP is hardcoded here. It has been redacted just for the sake
# of upload to a repository.

class NetControl:
    def __init__(self):
        self.imageHub = imagezmq.ImageHub()
        self.serverIP = 'IP'
        self.serverPORT = 'PORT'

    def startVideo(self):
        message = 'http://' + self.serverIP + ':' + self.serverPORT + '/startVideo'
        requests.get(message)

    def stopVideo(self):
        message = 'http://' + self.serverIP + ':' + self.serverPORT + '/stopVideo'
        requests.get(message)

    def getFrame(self):
        (rpiName, frame) = self.imageHub.recv_image()
        self.imageHub.send_reply(b'OK')

        return frame

    def setDriveForward(self):
        message = 'http://' + self.serverIP + ':' + self.serverPORT + '/driveForward'
        requests.get(message)

    def setDriveBackward(self):
        message = 'http://' + self.serverIP + ':' + self.serverPORT + '/driveBackward'
        requests.get(message)

    def setDriveStop(self):
        message = 'http://' + self.serverIP + ':' + self.serverPORT + '/driveStop'
        requests.get(message)

    def setSteerRight(self):
        message = 'http://' + self.serverIP + ':' + self.serverPORT + '/steerRight'
        requests.get(message)

    def setSteerLeft(self):
        message = 'http://' + self.serverIP + ':' + self.serverPORT + '/steerLeft'
        requests.get(message)

    def setSteerNeutral(self):
        message = 'http://' + self.serverIP + ':' + self.serverPORT + '/steerNeutral'
        requests.get(message)
        