# Listen to an MQTT feed and when a message is received 
# take pictures and save them to S3. 
#
# Using an RPi camera and two USB cameras.
#
# Copyright (c) 2017 MonoHelix Labs

import os
import sys
import multiprocessing
import subprocess
from time import sleep
from timeit import default_timer as timer
import boto3
from Adafruit_IO import Client
from Adafruit_IO import MQTTClient
import RPi.GPIO as GPIO

aio_key = os.environ['AIOKEY']
aio_user = os.environ['AIOUSER']
aio = Client(aio_key)
aio_mqtt = MQTTClient(aio_user, aio_key)
s3 = boto3.client('s3')
size = "2592x1944"
dev0 = "/dev/video0"
dev1 = "/dev/video1"
mqtt_feed_sub = 'fridgecam'
mqtt_feed_pub = 'fridgecamsnaps'
s3_bucket = 'fridge.monohelixlabs.com'
relay_pin = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)

def connected(client):
    print('Connected to AIO!  Listening for '+mqtt_feed_sub+' changes...')
    client.subscribe(mqtt_feed_sub)

def disconnected(client):
    print('Disconnected from AIO!')
    # mqtt_run()

def grab_usb_image(dev, opt0, opt1, size,fname):
    print('grab_usb_image', dev, fname)
    fpath = os.path.join('/tmp', fname)
    p = subprocess.Popen(["fswebcam","-q","-d",dev,opt0,opt1,"--no-banner","-r",size,fpath])
    p.wait()
    s3.upload_file(fpath, s3_bucket, fname)

def grab_rpi_image(fname):
    print('grab_rpi_image', fname)
    fpath = os.path.join('/tmp', fname)
    p = subprocess.Popen(["raspistill","-vf","-hf","-w","2592","-h","1944","-t","1","-o",fpath])
    p.wait()
    s3.upload_file(fpath, s3_bucket, fname)

def grab_images():
    start_time = timer()
    GPIO.output(relay_pin, GPIO.HIGH)
    pool = multiprocessing.Pool()
    pool.apply_async(grab_usb_image, (dev0, '--rotate', '90', "1944x2592", 'v0.jpg'))
    pool.apply_async(grab_usb_image, (dev1, '--rotate', '180', "2592x1944", 'v1.jpg'))
    pool.apply_async(grab_rpi_image, ('v2.jpg',))
    pool.close()
    pool.join()
    GPIO.output(relay_pin, GPIO.LOW)
    end_time = timer()
    delta_time = end_time - start_time
    print('Elapsed:',delta_time)
    aio.send(mqtt_feed_pub, delta_time)

def message(client, feed_id, payload):
    print('Feed {feed}  received new value: {message}'.format(feed=mqtt_feed_sub, message=payload))
    if payload == 'snapnow':
        grab_images()

def setup_mqtt():
    aio_mqtt.on_connect = connected
    aio_mqtt.on_disconnect = disconnected
    aio_mqtt.on_message = message

def mqtt_run():
    aio_mqtt.connect()
    for i in range(20):
        try:
            aio_mqtt.loop_blocking()
            break
        except:
            print('Error:', sys.exc_info()[0])
            print('Failed loop, waiting 5s...')
            sleep(5)
            continue

if __name__ == '__main__':
    setup_mqtt()
    mqtt_run()
