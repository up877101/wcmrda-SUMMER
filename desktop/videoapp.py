# A VideoApp class that is responsible for managing the display
# of the camera feed from the robot and the interation of the 
# user with the client application.

# import the necessary packages
from PIL import Image
from PIL import ImageTk
from imutils.video import VideoStream
from netControl import NetControl
import tkinter as tki
import tkinter.ttk as tkk
import time
import imutils
import numpy as np
import cv2
from debouncer import Debouncer

class VideoApp:
    def __init__(self):
        # start the video stream object then initialize the frame
        self.netController = NetControl()
        self.netController.startVideo()
        self.frame = None

        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None   

        # set a callback to handle when the window is closed
        self.root.wm_title("Robot Control App")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        # setup the key debouncer
        self.debouncer = Debouncer(self._pressed_cb, self._released_cb)
        self.root.bind('<KeyPress>', self.debouncer.pressed)
        self.root.bind('<KeyRelease>', self.debouncer.released)

        self.updateVideo()
    
    def updateVideo(self):
        # handles getting frame from imageHub on web server, 
        # then edits and updates GUI

        # grab the frame from the video stream and resize it to
        # have a maximum width of 1280 pixels
        self.frame = self.netController.getFrame()
        self.frame = imutils.resize(self.frame, width=1280)
        # OpenCV represents images in BGR order; however PIL
        # represents images in RGB order, so we need to swap
        # the channels, then convert to PIL and ImageTk format
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # convert image to displayable image in GUI component
        self.frame = Image.fromarray(self.frame)
        self.frame = ImageTk.PhotoImage(self.frame)

        # if the panel is not None, we need to initialize it
        if self.panel is None:
            self.panel = tki.Label(image=self.frame)
            self.panel.image = self.frame
            self.panel.pack(side="left", padx=10, pady=10)

        # otherwise, simply update the panel
        else:
            self.panel.configure(image=self.frame)
            self.panel.image = self.frame

        # call this function again after 41 ms ~= 24fps
        self.root.after(41, self.updateVideo)

    def _pressed_cb(self, event):
        # captures key press events and makes webserver call depending
        # on direction of desired movement
        if event.keycode == 87:
            self.netController.setDriveForward()
        elif event.keycode == 83:
            self.netController.setDriveBackward()
        elif event.keycode == 65:
            self.netController.setSteerLeft()
        elif event.keycode == 68:
            self.netController.setSteerRight()

    def _released_cb(self, event):
        # captures key release events and makes webserver call depending
        # on direction of desired movement
        if event.keycode == 87:
            self.netController.setDriveStop()
        elif event.keycode == 83:
            self.netController.setDriveStop()
        elif event.keycode == 65:
            self.netController.setSteerNeutral()
        elif event.keycode == 68:
            self.netController.setSteerNeutral()

    def onClose(self):
        # cleanup the camera and allow the rest of the quit process to continue
        self.netController.stopVideo()
        self.root.quit()