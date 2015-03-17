#!/usr/bin/python

import LPD8806

led = LPD8806.strand()

led.fill(0, 0, 0)
led.update()