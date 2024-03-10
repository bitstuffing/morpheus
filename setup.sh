#!/bin/bash

# pip dependencies for neopixels dependencies for raspberrypi
sudo apt install libopenjp2-7 libopenblas0 -Y

# adafruit install instructions for neopixels: https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
pip install rpi_ws281x adafruit-circuitpython-neopixel
pip install --force-reinstall adafruit-blinka

# project ones
pip install -r requirements.txt

# fonts
wget -P types https://github.com/matomo-org/travis-scripts/raw/master/fonts/Arial.ttf
wget -P types https://github.com/tsenart/sight/raw/master/fonts/Consolas.ttf

# bluetooth
sudo apt install bluez pulseaudio-module-bluetooth
