# Retrieve weight from weight scales using HX711.
#
# Code is based on the HX711 Python Library for Raspberry Pi 
# written by Philip Whitfield "https://github.com/underdoeg/" 
# modified by tatobari "https://github.com/tatobari/hx711py"
# and further adapted to Python 3 in the MonoHelix Labs fork 
# "https://github.com/MonoHelixLabs/hx711py"
#
# Note that you need the HX711.py from repo mentione above
# to be in the same folder as this file.

import RPi.GPIO as GPIO
import time
import os
import sys
from hx711 import HX711
from Adafruit_IO import Client

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

hx1 = HX711(5, 6)
hx2 = HX711(8, 7)

aio_key = os.environ['AIOKEY']
aio = Client(aio_key)

feed_name1 = 'scalepos2'
feed_name2 = 'scalepos3'

hx1.set_reading_format("LSB","MSB")
hx2.set_reading_format("LSB","MSB")

hx1.set_reference_unit(-2037)
hx2.set_reference_unit(-2037)

hx1.reset()
hx1.tare()
hx2.reset()
hx2.tare()

while True:
    try:
        val1 = hx1.get_weight(5)
        print("val1:" + str(val1))
        aio.send(feed_name1, int(val1))

        hx1.power_down()
        hx1.power_up()

        val2 = hx2.get_weight(5)
        print("val2:" + str(val2))
        aio.send(feed_name2, int(val2))

        hx2.power_down()
        hx2.power_up()
        
        time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

