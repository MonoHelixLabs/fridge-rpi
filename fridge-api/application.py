import time
from Adafruit_IO import Client
from Adafruit_IO import MQTTClient
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

aio_key = ''
aio_user = ''
aio_rest = Client(aio_key)
aio_mqtt = MQTTClient(aio_user, aio_key)
mqtt_feed = 'fridgecam'
mqtt_message = 'snapnow'
min_sec_between_snaps = 30
start_time = 0

def connected(client):
    print('Connected to AIO!')

def disconnected(client):
    print('Disconnected from AIO!')
    mqtt_run()

def setup_mqtt():
    aio_mqtt.on_connect = connected
    aio_mqtt.on_disconnect = disconnected

def mqtt_run():
    aio_mqtt.connect()
    aio_mqtt.loop_background()

def send_message():
    global start_time
    end_time = time.time()
    time_delta = end_time - start_time
    print(start_time, end_time, time_delta)
    if time_delta > min_sec_between_snaps:
        mqtt_run()
        aio_mqtt.publish(mqtt_feed, mqtt_message)
        start_time = end_time
        return "Request sent"
    return "Too soon, wait " + str(int(min_sec_between_snaps - time_delta)) + " sec"

@application.route('/')
def hello():
    return 'Hello World!'

@application.route('/snapnow')
@cross_origin()
def snapnow():
    return send_message()

@application.route('/status', methods=['GET'])
@cross_origin()
def status():
    top = aio_rest.receive('tmptop')
    mid = aio_rest.receive('tmpmiddle')
    bot = aio_rest.receive('tmpbottom')
    temp = round((float(top.value) + float(mid.value) + float(bot.value))/3.0,1)
    return jsonify({'status':{'temperature':str(temp)}})

@application.route('/milkstatus', methods=['GET'])
@cross_origin()
def milkstatus():
    milkscale1 = aio_rest.receive('scalepos2')
    milkscale2 = aio_rest.receive('scalepos3')
    liters = round((float(milkscale1.value) + float(milkscale2.value))/1000.,2)
    return jsonify({'status':{'liters':str(liters)}})

if __name__ == "__main__":
    setup_mqtt()
    mqtt_run()
    application.run()