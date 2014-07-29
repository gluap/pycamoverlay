# Raspberry pi dashcam project
This project contains software to record video in sync with GPS data on a raspberry pi and later add  a HUD-Like overlay with map and GPS information in post processing. There are lots of dependencies.

# Stuff you need
* python-ant driver (https://github.com/cowboy-coders/python-ant)
* ant-stick
* mapnik for python 
* a map style (I use https://github.com/andrewharvey/osm-hybrid-carto because it is half-transparent and therefore perfectly suited for a video overlay)
* openstreetmap data for the area
* ffmpeg / avconv
* PIL
* wiringPi (http://wiringpi.com/) for the ultrasonic distance sensor