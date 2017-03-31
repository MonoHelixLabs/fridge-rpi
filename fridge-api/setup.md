Setup env for RESTful Fridge API

# Install required packages

```
brew install python3
python3 -m venv ~/.virtualenvs/fridge-api
source ~/.virtualenvs/fridge-api/bin/activate
pip install flask
pip install flask-cors
pip install paho-mqtt
# pip install adafruit-io
```

To run the application locally:

```
python application.py
```

# Setup Elastic Beanstalk Python project

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
