#!/usr/bin/env python

import RPi.GPIO as GPIO, feedparser, time, LPD8806

DEBUG = 1

USERNAME = "nyscicubetest"     # just the part before the @ sign, add yours here
PASSWORD = "cubetest"     

NEWMAIL_OFFSET = 0        # my unread messages never goes to zero, yours might
MAIL_CHECK_FREQ = 5      # check mail every 60 seconds

led = LPD8806.strand()

while True:

        newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom")["feed"]["fullcount"])

        if DEBUG:
                print "You have", newmails, "new emails!"

        if newmails > NEWMAIL_OFFSET:
                led.fill(255, 0, 0)
                led.update()
        else:
                led.fill(0, 255, 0)
                led.update()

        time.sleep(MAIL_CHECK_FREQ)
