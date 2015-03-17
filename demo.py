#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 30;
led = LEDStrip(num)
white = Color(255, 255, 255)
green = Color(0, 255, 0)

led.all_off()
led.fill(white,0,5)
led.fill(green,6,11)
led.update()