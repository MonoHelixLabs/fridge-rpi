import multiprocessing
import subprocess
import os
from timeit import default_timer as timer
import boto3
from Adafruit_IO import Client

aio_key = os.environ['AIOKEY']
aio = Client(aio_key)
s3 = boto3.client('s3')
size = "1920x720"
dev0 = "/dev/video0"
dev1 = "/dev/video1"
mqtt_feed = 'new-feed'
s3_bucket = 'myfridge.monohelixlabs.com'

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
    pool = multiprocessing.Pool()
    pool.apply_async(grab_usb_image, (dev0, 'v0.jpg'))
    pool.apply_async(grab_usb_image, (dev1, 'v1.jpg'))
    pool.apply_async(grab_rpi_image, ('v2.jpg',))
    pool.close()
    pool.join()
    end_time = timer()
    delta_time = end_time - start_time
    print('Elapsed:',delta_time)
    aio.send(mqtt_feed, delta_time)
