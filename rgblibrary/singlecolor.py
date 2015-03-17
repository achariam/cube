#!/usr/bin/python

import LPD8806

led = LPD8806.strand()

while True:
	led.wheel(0,30)
	led.update()
