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

[Dockerfile](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Dockerfile) contains the Docker instructions. There are two lines commented out, which should be uncommented if used for local deployment on port 9696. Currently it is set for remote deployment on Heroku, and so no port is set.

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
To deploy on Heroku, comment out the following two lines of [Dockerfile](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Dockerfile):
```
#EXPOSE 9696  #(For local deployment)

#ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict_vowel:app" ]  #(For local deployment)
```
and uncomment:
```
ENTRYPOINT [ "gunicorn", "predict_vowel:app" ]
```
In [predict_vowel.py](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/predict_vowel.py) change the variable DEPLOY to equal 'heroku':
```
DEPLOY = 'heroku'
```
Then
```
git push heroku main
```
will build the Docker file and push it up to Heroku.

## Accessing the Heroku app
The deployed app can be accessed on Heroku at [https://zoomcamp-midterm-heroku.herokuapp.com/predict](https://zoomcamp-midterm-heroku.herokuapp.com/predict) with a test page at [https://zoomcamp-midterm-heroku.herokuapp.com/welcome](https://zoomcamp-midterm-heroku.herokuapp.com/welcome).

The [jupyter notebook](https://github.com/woodwardmw/MLZoomCamp-Midterm/blob/main/Mid-term%20Vowel%20Prediction%20Project.ipynb) contains the following code to send a POST request for one particular randomly chosen example to the Heroku app and receive a response:
```
# Pick a random example from the test set

random_index = random.randint(0, df_test.shape[0] - 1)
random_index

example = df_test.drop(['speaker', 'vowel'], axis=1).iloc[[random_index,]]
example = example.to_dict()

import requests
url = 'https://zoomcamp-midterm-heroku.herokuapp.com/predict'
response = requests.post(url, json=example)
result = response.json()
result
```
## One simple example to verify the Heroku app is working
If you haven't imported the data, and want to just run one example, here is one to run:
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
