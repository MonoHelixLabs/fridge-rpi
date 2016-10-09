import os
import sys
import multiprocessing
import subprocess
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
size = "1920x720"
dev0 = "/dev/video0"
dev1 = "/dev/video1"
mqtt_feed = 'fridgecam'
s3_bucket = 'fridge.monohelixlabs.com'
relay_pin = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)

def connected(client):
    print('Connected to AIO!  Listening for '+mqtt_feed+' changes...')
    client.subscribe(mqtt_feed)

def disconnected(client):
    print('Disconnected from AIO!')
    # mqtt_run()

def grab_usb_image(dev, fname):
    print('grab_usb_image', dev, fname)
    fpath = os.path.join('/tmp', fname)
    p = subprocess.Popen(["fswebcam","-q","-d",dev,"--no-banner","-r",size,fpath])
    p.wait()
    s3.upload_file(fpath, s3_bucket, fname)

def grab_rpi_image(fname):
    print('grab_rpi_image', fname)
    fpath = os.path.join('/tmp', fname)
    p = subprocess.Popen(["raspistill","-w","1440","-h","720","-t","1","-o",fpath])
    p.wait()
    s3.upload_file(fpath, s3_bucket, fname)

def grab_images():
    start_time = timer()
    GPIO.output(relay_pin, GPIO.HIGH)
    pool = multiprocessing.Pool()
    pool.apply_async(grab_usb_image, (dev0, 'v0.jpg'))
    pool.apply_async(grab_usb_image, (dev1, 'v1.jpg'))
    pool.apply_async(grab_rpi_image, ('v2.jpg',))
    pool.close()
    pool.join()
    GPIO.output(relay_pin, GPIO.LOW)
    end_time = timer()
    delta_time = end_time - start_time
    print('Elapsed:',delta_time)
    aio.send(mqtt_feed, delta_time)

def message(client, feed_id, payload):
    print('Feed '+mqtt_feed+' received new value:', payload)
    if payload == 'snapnow':
        grab_images()

def setup_mqtt():
    aio_mqtt.on_connect = connected
    aio_mqtt.on_disconnect = disconnected
    aio_mqtt.on_message = message

def mqtt_run():
    aio_mqtt.connect()
    aio_mqtt.loop_blocking()

if __name__ == '__main__':
    setup_mqtt()
    mqtt_run()
