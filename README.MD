# Raspberry pi dashcam
This project contains software to record video in sync with GPS and other data on a raspberry pi and later add  a HUD-Like overlay with map and GPS information in post processing. There are lots of dependencies.

# Stuff you need for recording on the pi
* python-ant driver (https://github.com/cowboy-coders/python-ant)
* ant-stick (optional)
* wiringPi (http://wiringpi.com/) for the ultrasonic distance sensor
* gpsd
* bluetooth or other GPS device working with gpsd


# stuff you need for postprocessing (to produce nice video overlays)
* mapnik for python 
* a map style (I use https://github.com/andrewharvey/osm-hybrid-carto because it is half-transparent and therefore perfectly suited for a video overlay)
* openstreetmap data for the area
* ffmpeg / avconv
* PIL
