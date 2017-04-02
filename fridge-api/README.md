# Setup env for RESTful Fridge API

## About
The code in this folder shows how to create a Fridge API that stands as a layer between the backend and interfaces such as a web page or an Alexa skill.

## Install required packages

```
brew install python3
python3 -m venv ~/.virtualenvs/fridge-api
source ~/.virtualenvs/fridge-api/bin/activate
pip install flask
pip install flask-cors
pip install paho-mqtt
# pip install adafruit-io
```

(Note: The adafruit-io package required some fixes, therefore it is included as a folder and does not require installation. Credit for the Adafruit IO Python Client Library code goes to Adafruit, code repo ```https://github.com/adafruit/io-client-python```. If the fix is done in the release in the future, then switch to normal installation.)

To run the application locally:

```
python application.py
```

## Setup Elastic Beanstalk Python project

```
pip install awsebcli
pip freeze > requirements.txt
eb init
eb create
```

To commit changes:

```
eb deploy
```

To see app in browser:

```
eb open
```

## Make changes to the application and deploy to EB


```
source ~/.virtualenvs/fridge-api/bin/activate
python application.py
eb deploy
eb open
```

## Links

* More info on AWS EB CLI: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-getting-started.html
* Example for deploying Python Flask app on EB: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
