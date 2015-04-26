# Raspberry pi dashcam
This project contains software to record video in sync with GPS and other data on a raspberry pi and later add  a HUD-Like overlay with map and GPS information in post processing. There are lots of dependencies.

## requirements for recording on the pi
* gpsd
* picamera
* bluetooth or other GPS device working with gpsd

**Optional: If you want to record data from sports devices (heart rate belt, temperature, cadence etc.) you need this:**

* python-ant driver (https://github.com/cowboy-coders/python-ant)
* ant-usb-stick

**Optional: If you want distance measurements using ultrasonic distance meter (for measuring side distance of cars overtaking you)**

* wiringPi (http://wiringpi.com/) for the ultrasonic distance sensor
* an ultrasonic distance sensor https://secure.robotshop.com/en/hc-sr04-ultrasonic-range-finder.html

## requirements for postprocessing (rendering video overlays)
* mapnik for python 
* a map style (I use https://github.com/andrewharvey/osm-hybrid-carto because it is half-transparent and therefore perfectly suited for a video overlay)
* openstreetmap data for the area
* ffmpeg / avconv
* PIL


### Preparation for map generation (tested on Ubuntu 12.04/14.04)
To have nice, half-transparent pieces of map like I use, you should first follow https://www.mapbox.com/blog/create-a-custom-map-of-your-city-in-30-minutes-with-tilemill-and-openstreetmap/ to prepare your computer for the rendering of the map  (download map data, prepare a database). These steps tage about 30 minutes, depending on the size of the map area you need it can be longer or shorter.
https://switch2osm.org/loading-osm-data/


When you are done you can install the osmt transparent openstretmap style from https://github.com/andrewharvey/osm-hybrid-carto/
(follow the manual there)

Finally install mapnik

```
#!bash
sudo aptitude install python-mapnik2
```

under ubuntu 12.04 you might have to install some packages using pip (imposm for instance) or from the mapnik repository
```
sudo add-apt-repository ppa:mapnik/v2.2.0
sudo apt-get update
sudo apt-get install libmapnik libmapnik-dev mapnik-utils python-mapnik
```

under 14.04 try the versions from the ubuntu repositories:
```sudo aptitude install imposm python-imposm libav-tools```