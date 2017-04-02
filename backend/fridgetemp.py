# Read temperature values and send them to Adafruit IO MQTT feeds.
#
# Using three DS18B20 temperature sensors.
#
# Copyright (c) 2017 MonoHelix Labs


import os
import sys
from time import sleep
from Adafruit_IO import Client
from Adafruit_IO import MQTTClient

base_dir = '/sys/bus/w1/devices/'
aio_key = os.environ['AIOKEY']
aio_user = os.environ['AIOUSER']
aio = Client(aio_key)

feed_map = {
    'tmptop':'28-011562093fff/w1_slave',
    'tmpmiddle':'28-0115625258ff/w1_slave',
    'tmpbottom':'28-0315622969ff/w1_slave'
}

def read_temp_raw(device_file):
    f = open(os.path.join(base_dir,device_file), 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

if __name__ == '__main__':
    while True:
        for feed_name, device_file in feed_map.items():
            temp_c = read_temp(device_file)
            aio.send(feed_name, temp_c)
        sleep(60)
