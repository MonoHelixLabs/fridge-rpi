
Static web page setup

# Install `MQTT.js`
Use `npm` to install MQTT.js and its dependencies:
```
mac:~ radu$ mkdir fridgecam_webclient
mac:fridgecam_webclient radu$ cd ~/fridgecam_webclient/
mac:fridgecam_webclient radu$ npm install mqtt
mac:fridgecam_webclient radu$ cd node_modules/mqtt
mac:mqtt radu$ npm install .

```
# Bundle `MQTT.js` with `webpack`
Bundle `MQTT.js` with `webpack`:
```
mac:mqtt radu$ npm install -g webpack
mac:mqtt radu$ webpack mqtt.js ./browserMqtt.js --output-library mqtt
```
Deploy in destination directory:
```
mac:mqtt radu$ cp browserMqtt.js ~/fridgecam_webclient/
```
