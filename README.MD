# Raspberry pi dashcam
This project contains software to record video in sync with GPS and other data on a raspberry pi and later add  a HUD-Like overlay with map and GPS information in post processing. There are lots of dependencies.

## requirements for recording on the pi
* gpsd
**Optional: If you want to record data from sports devices (heart rate belt, temperature, cadence etc.) you need this:**
* python-ant driver (https://github.com/cowboy-coders/python-ant)
* ant-stick (optional)
**Optional: If you want distance measurements using ultrasonic distance meter (for measuring side distance of cars overtaking you)**
* wiringPi (http://wiringpi.com/) for the ultrasonic distance sensor
* bluetooth or other GPS device working with gpsd
* picamera


## requirements for postprocessing (rendering video overlays)
* mapnik for python 
* a map style (I use https://github.com/andrewharvey/osm-hybrid-carto because it is half-transparent and therefore perfectly suited for a video overlay)
* openstreetmap data for the area
* ffmpeg / avconv
* PIL