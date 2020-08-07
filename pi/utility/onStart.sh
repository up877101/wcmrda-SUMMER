#!/bin/bash
# script that runs on the raspberry pi when it starts
# this starts the web server and prepares the device
# to recieve commands from the client application.

cd ~
source .profile
workon wcmrda
cd ~/Documents/repos/wirelesscontrol/pi
python3 picontroller.py
