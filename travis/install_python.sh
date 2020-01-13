#!/bin/bash

set -e
source travis/travis_retry.sh
echo "---------------------------------"
echo "-------- setup wine prefix ------"
echo "---------------------------------"
# We need the developer version of wine.  We need at least version 4.14 (see link).
# This is the earliest version I've seen reported to work with python3 well
# Without this, we'd have to run the embedded install of python which is riddled
# with annoying issues.

# see: https://appdb.winehq.org/objectManager.php?sClass=version&iId=38187

#echo "------ Installing required apt packages ------"
#apt update
#apt install -y wget gnupg software-properties-common apt-utils

echo "------ Add latest wine repo ------"
# Need at least wine 4.14 to install python 3.7
#bash travis/travis_retry.sh sudo dpkg --add-architecture i386
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
sudo apt update

# Add repo for faudio package.  Required for winedev
sudo add-apt-repository -y ppa:cybermax-dexter/sdl2-backport

echo "-------- Install wine-dev ------"

sudo apt-get install -y winehq-devel winetricks

echo "------ Download python ------"
wget https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe
#wget https://www.python.org/ftp/python/3.7.6/python-3.7.6.exe

echo "------ Init wine prefix ------"
WINEPREFIX=~/.wine64 WINARCH=win64 winetricks \
    corefonts \
   # win10

# Setup dummy screen
echo "------ Setup Dummy Screen ------"
#sudo Xvfb :0 -screen 0 1024x768x16 &
#jid=$!

echo "------ Install python ------"
#export DISPLAY=:0.0
xvfb-run WINEPREFIX=~/.wine64 wine cmd /c python-3.6.8-amd64.exe /quiet PrependPath=1
echo "Python Installation complete!"
# Display=:0.0 redirects wine graphical output to the dummy display.
# This is to avoid docker errors as the python installer requires a display,
# even when quiet install is specified.