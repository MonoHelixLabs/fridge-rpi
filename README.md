# fridge-rpi

A smart fridge prototype running on Raspberry Pi.

![alt tag](https://github.com/MonoHelixLabs/fridge-rpi/blob/master/bucket/logo.png)

## Prototype

An old fridge has been retrofitted with a Raspberry Pi 2 Model B, 3 wide-lens cameras (1 Raspberry Pi camera and 2 USB cameras), 3 temperature sensors (DS18B20), and 2 weight scales (3-wire load cells). 

The readings from the sensors are sent periodically to Adafruit IO through MQTT and the images are saved to Amazon S3. 

## Interfaces

The fridge's [web page](http://fridge.monohelixlabs.com) provides a user interface to explore this data and get insights about the status of the fridge. It allows for remote exploration of the content of the fridge and checking exactly how much milk is left on the fridge door. 

Alerts can be set up with for example [IFTTT](http://ifttt.com ) to be notified when the temperature goes above a certain threshold, so you know if the door has been left open and when.

An [Alexa MyFridge skill](https://github.com/MonoHelixLabs/alexa-skills-myfridge) can provide status info about the fridge on request through voice interaction. 
