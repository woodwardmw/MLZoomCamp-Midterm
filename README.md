# MLZoomCamp Midterm Project
## Table of Contents
 * [Introduction](#introduction)
 * [Running the Project](#running-the-project)
    * [Local deployment](#local-deployment)
    * [Remote deployment on Heroku](#remote-deployment-on-heroku)
 * [Accessing the Heroku app](#accessing-the-heroku-app)
 * [One simple example to verify the Heroku app is working](#one-simple-example-to-verify-the-heroku-app-is-working)
## Introduction
In phonetics, it is generally known that the resonant frequencies of the vocal tract of the speaker can be used to determine the quality of the vowel being spoken.

Here I have taken data of English speakers pronouncing eleven different vowels in their language. The data is taken from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Connectionist+Bench+%28Vowel+Recognition+-+Deterding+Data%29).

The data consists of 15 speakers each pronouncing 11 vowels, six times each. The phonetic data is then processed, and classified as formats from f0 to f9, and recorded together with data about which speaker has made the sound and the sex of the speaker.

The data I used came from [here](http://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/vowel/vowel-context.data).

## Running the Project
The analysis, model selection and hyperparameters tuning are contained in the [jupyter notebook](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Mid-term%20Vowel%20Prediction%20Project.ipynb). These scripts are cleaned up as a python file here: [Mid-term Vowel Prediction Project.py](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Mid-term%20Vowel%20Prediction%20Project.py)

The final model is exported to [vowel-model.bin](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/vowel-model.bin).

The script to deploy the model using flask is contained in [predict_vowel.py](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/predict_vowel.py).

[Pipfile](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Pipfile) and [Pipfile.lock](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Pipfile.lock) set up the pipenv environment. These can be called by Docker. The virtual environment can be activated by running
```
pipenv shell
```

[Dockerfile](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Dockerfile) contains the Docker instructions. Note that I deployed both locally and remotely on Heroku, and each required a slightly different Dockerfile. (Specifically Heroku requires that the port not be set). There are two lines commented out in the version of the Dockerfile in this repository, which should be uncommented if used for local deployment on port 9696. Currently it is set for remote deployment on Heroku, and so no port is set.

### Local deployment
To deploy locally, uncomment the following two lines of [Dockerfile](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Dockerfile):
```
#EXPOSE 9696  #(For local deployment)

#ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict_vowel:app" ]  #(For local deployment)
```
and comment out:
```
ENTRYPOINT [ "gunicorn", "predict_vowel:app" ]
```
In [predict_vowel.py](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/predict_vowel.py) change the variable
```
DEPLOY
```
to something other than 'heroku'.

To build, from this directory run: 

```
sudo docker build -t zoomcamp-midterm .
```

To run:

```
sudo docker run -it --rm -p 9696:9696 zoomcamp-midterm:latest
```
### Remote deployment on Heroku
To deploy on Heroku, you can use the version of the [Dockerfile](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Dockerfile) in this repository, which has the following two lines commented out:
```
#EXPOSE 9696  #(For local deployment)

#ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict_vowel:app" ]  #(For local deployment)
```
and this line instead:
```
ENTRYPOINT [ "gunicorn", "predict_vowel:app" ]
```
In [predict_vowel.py](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/predict_vowel.py) ensure the variable DEPLOY is to equal 'heroku':
```
DEPLOY = 'heroku'
```
Then I used
```
git push heroku main
```
to build the Docker file and push it up to my Heroku deployment.

## Accessing the Heroku app
The deployed app can be accessed on Heroku at [https://zoomcamp-midterm-heroku.herokuapp.com/predict](https://zoomcamp-midterm-heroku.herokuapp.com/predict) with a test page at [https://zoomcamp-midterm-heroku.herokuapp.com/welcome](https://zoomcamp-midterm-heroku.herokuapp.com/welcome).

The simplest way to verify it is working is to run [predict_test.py](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/predict_test.py). This script takes a random example from the test data, and outputs the actual vowel, and the predicted vowel via the Heroku deployment.

[Accessing the Heroku app via predict_test.py](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/images/Screenshot_of_predict_script.png)
## One simple example to verify the Heroku app is working
Otherwise, if you want to just run one example, here is one to run:
```
example = {'sex': {967: 1},
 'f0': {967: -3.325},
 'f1': {967: 2.141},
 'f2': {967: -0.528},
 'f3': {967: 0.439},
 'f4': {967: 0.099},
 'f5': {967: 0.321},
 'f6': {967: 0.217},
 'f7': {967: 0.135},
 'f8': {967: -1.388},
 'f9': {967: 0.746}}

import requests
url = 'https://zoomcamp-midterm-heroku.herokuapp.com/predict'
response = requests.post(url, json=example)
result = response.json()
result
```
