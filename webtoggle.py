#!/usr/bin/python

from twisted.web.server import Site       #import twisted stuff
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File

import threading 

import feedparser
import random
 
from time import sleep
from LPD8806 import *

from secrets import *

import forecastio

api_key = DarkSkyAPIKey
lat = 40.73444444444444
lng = -74.17444444444445 #Newark, NJ

num = 30;
led = LEDStrip(num)
white = Color(255, 255, 255)
blue = Color(0, 0, 255)

USERNAME = "email"     # just the part before the @ sign, add yours here
PASSWORD = "password"
MODE = 0
BULB = 0

globaltemp = 0


#BOOTUPSEQUENCE----

for i in range(150):
    led.anim_rainbow_cycle()
    led.update()

led.fillOff()


#BOOTUPSEQUENCE END----
 
class lampAPI(Resource):
   def render_GET(self, request):

            global MODE
            global BULB

            if 'light' in request.args:                        #'light' is the URL variable
                        MODE = -1
                        if request.args['light'][0] == "on":     #Did the client put 'off' in the light var?
                                led.fill(white)
                                led.update()       #turn the lamp on
                                BULB = 1
                                return " <html> light on </html> "                 #tell the browser/client that we did it
                        if request.args['light'][0] == "off":      #Did the client put 'on' in the light var? 
                                led.all_off()
                                led.update()        #turn the lamp on   
                                BULB = 0 
                                return " <html> light off </html> "                  #tell the browser/client that we did it
                        if request.args['light'][0] == "toggle":
                                if BULB == 1:
                                    BULB = 0
                                    led.all_off()
                                    led.update() 
                                    return "<html> light off </html>"
                                elif BULB == 0:
                                    BULB = 1
                                    led.fill(white)
                                    led.update()  
                                    return "<html> light on </html>"



            if 'mode' in request.args:
                if request.args['mode'][0] == "mail":
                    MODE = 1
                    return "<html>Checking Mail</html>"
                if request.args['mode'][0] == "rainbow":
                    MODE = 2
                    return "<html>Rainbow</html>"
                if request.args['mode'][0] == "weather":
                    MODE = 3
                    return "<html>Weather Mode</html>"


def weatherNow():
    while 1:


        global globaltemp
        forecast = forecastio.load_forecast(api_key, lat, lng)
        forecastNow = forecast.currently()
        globaltemp = forecastNow.temperature
        print globaltemp
        print forecastNow.summary
        sleep(180) #Check every 3 minutes



def pulse(temp):

        if temp <= 30:
            step = 0.01
            level = 0.01
            dir = step
            while level >= 0.0:
                led.fill(Color(255, 255, 255, level))
                led.update()
                if(level >= 0.99):
                   dir = -step
                level += dir    #30 degrees and under = white

        elif temp <= 40:
            step = 0.01
            level = 0.01
            dir = step
            while level >= 0.0:
                led.fill(Color(130, 200, 255, level))
                led.update()
                if(level >= 0.99):
                   dir = -step
                level += dir    #31-40 degrees = light blue


        elif temp <= 50:
            step = 0.01
            level = 0.01
            dir = step
            while level >= 0.0:
                led.fill(Color(0, 0, 255, level))
                led.update()
                if(level >= 0.99):
                   dir = -step
                level += dir    #41-50 degrees = blue


        elif temp <= 60:
            step = 0.01
            level = 0.01
            dir = step
            while level >= 0.0:
                led.fill(Color(0, 255, 125, level))
                led.update()
                if(level >= 0.99):
                   dir = -step
                level += dir    #51-60 degrees = blueish green


        elif temp <= 70:
            step = 0.01
            level = 0.01
            dir = step
            while level >= 0.0:
                led.fill(Color(0, 255, 0, level))
                led.update()
                if(level >= 0.99):
                   dir = -step
                level += dir    #61-70 degrees = green


        elif temp <= 80:
            step = 0.01
            level = 0.01
            dir = step
            while level >= 0.0:
                led.fill(Color(200, 255, 50, level))
                led.update()
                if(level >= 0.99):
                   dir = -step
                level += dir    #71-80 degrees = yellowish green


        elif temp <= 90:
            step = 0.01
            level = 0.01
            dir = step
            while level >= 0.0:
                led.fill(Color(255, 255, 0, level))
                led.update()
                if(level >= 0.99):
                   dir = -step
                level += dir    #81-90 degrees = yellow


        else:
            step = 0.01
            level = 0.01
            dir = step
            while level >= 0.0:
                led.fill(Color(255, 0, 0, level))
                led.update()
                if(level >= 0.99):
                   dir = -step
                level += dir    #90+ degrees = red





def emailnotify():
    newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom")["feed"]["fullcount"])
    if newmails > 0:
        step = 0.01
        level = 0.01
        dir = step
        while level >= 0.0:
            led.fill(Color(0, 0, 255, level))
            led.update()
            if(level >= 0.99):
               dir = -step
            level += dir
            sleep(0.01)

    else:
        step = 0.01
        level = 0.01
        dir = step
        while level >= 0.0:
            led.fill(Color(255, 255, 255, level))
            led.update()
            if(level >= 0.99):
               dir = -step
            level += dir
            sleep(0.01)

def rainbow():
    led.anim_rainbow_cycle()
    led.update()



weatherMonitor = threading.Thread(target=weatherNow)
weatherMonitor.daemon = True
weatherMonitor.start()


root = File("cubewww")           #Create a folder for web interface 
root.putChild("API", lampAPI())  #Create a child that will handle requests (the second argument must be the class name)
factory = Site(root)             #Initialize the twisted object 
reactor.listenTCP(80, factory)   #Choose the port to listen on (80 is standard for HTTP) 
reactor.startRunning(False)

while True:
    reactor.iterate()
    if MODE == 0:
        led.all_off()
        led.update()
    if MODE == 1:
        emailnotify()
    if MODE == 2:
        rainbow()
    if MODE == 3:
        pulse(globaltemp)


