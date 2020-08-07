#!/bin/bash
# script that ensures both the desktop (for desktop app) and pi client are
# setup with the required dependencies to run the software

sudo apt-get update

echo "Installing git"
sudo apt-get install git

echo "Installing compilation tools"
sudo apt-get install gcc g++ cmake

echo "Upgrading Python 3"
sudo apt-get upgrade python3

echo "Installing build-essential, libssl-dev, libffi-dev and python3-dev"
sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev

echo "Installing pip3"
sudo apt-get install -y python3-pip
python3 -m pip install --upgrade pip

echo "Installing scientific computing packages"
pip3 install numpy scipy matplotlib ipython jupyter pandas sympy nose

echo "Installing required packages for GTK"
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libgtk-3-dev

echo "Installing support for extra file formats"
sudo apt-get install -y libpng-dev libjpeg-dev libopenexr-dev libtiff-dev libwebp-dev

echo "Installing imagezmq dependencies"
pip3 install opencv-contrib-python zmq imutils

echo "Checking repos directory exists"
if [ ! -d "~/repos" ]
then
    mkdir ~/repos
fi

cd ~/repos

echo "Checking imagezmq exists"
if [ ! -d "/imagezmq" ]
then
    git clone https://github.com/jeffbass/imagezmq.git
fi

echo "Checking wcmrda exists"
if [ ! -d "/wcmrda" ]
then
    git clone https://github.com/up877101/wcmrda-SUMMER.git
    cd wcmrda
    # ln -s creates a symlink to the imagezmq lib 
    ln -s ~/repos/imagezmq/imagezmq imagezmq
fi
