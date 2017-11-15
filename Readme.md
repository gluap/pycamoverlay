# Raspberry pi dashcam


This project contains software to record video in sync with GPS and
other data on a raspberry pi and later add  a HUD-Like overlay with
map and GPS information as well as fitness sensor data in post processing. 

Find a demo video of what this project does on: https://www.youtube.com/watch?v=swLGyjKVgmQ 
False colors are caused by the camera, which is a model without infrared filter.

The main complication of recording video and data in sync is the 
fluctuating framerate on a raspberry. To overcome the problem, the recorded
each recorded datapoint is stored together with the current frame number
at the time of recording the data point.

In post processing, since so far there seem to be no python around for
adding overlays to video files (at the time of creation of this project in 2014),
ffmpeg is used to transcode the video to a raw binary data stream which is
then modified by means of the python image library, and subsequently fed
back as a binary stream to ffmpeg for encoding. This was by far the fastest
method I could come up with, allowing near-realtime transcoding on my laptop.

There are lots of 
dependencies for the postprocessing software overlaying the HUD, 
most of it related to generating a semi-transparent map from 
OpenStreetmap data. Find below how to solve some of them.


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


### Setting up the GPS as a source of system time for the PI
(assuming a serial GPS that has pps[pulse per second] output, for instance this: https://thepihut.com/products/gps-module-with-enclosure

- install gpsd
- install chrony
- systemctl disable systemd-timesyncd *optional, to make the GPS the only source of time. Makes it easier to test
whether time via gpsd/chrony works correctly.*

# setting up database docker

sudo docker build . -t postgres-osm
sudo docker run -d --name postgres-osm -v pgsql_data:/var/lib/postgresql postgres-osm:latest

# setting up docker for video conversion

install postgres-osm
install postgres-client
install osm2pgsql



# docker for rendering?
install osmt
install librsvg2-bin

