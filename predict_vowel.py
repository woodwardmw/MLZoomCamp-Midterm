import pickle
from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd

model_file = 'vowel-model.bin'
with open (model_file, 'rb') as f_in:
    model = pickle.load(f_in)

DEPLOY = 'heroku'

app = Flask('vowel')

@app.route('/welcome', methods=['GET'])
def welcome():
    welcome_msg = "<h1>Welcome to your application deployed as Docker container on heroku</h1>"
    return welcome_msg

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    X = pd.DataFrame.from_dict(data)
    y_pred = model.predict(X)[0]
    vowel = convert_to_vowel(int(y_pred))
    result = {'Prediction': str(vowel)}
    return jsonify(result)

def convert_to_vowel(vowel_int):
    convert = {
    0: 'hid',
	1: 'hId',		
	2: 'hEd',
	3: 'hAd',		
	4: 'hYd',		
	5: 'had',		
	6: 'hOd',		
	7: 'hod',		
	8: 'hUd',		
	9: 'hud',		
	10: 'hed'
    }
    return convert.get(vowel_int, "No vowel given")


if __name__ == '__main__':
    if DEPLOY == 'heroku':
        port = int(os.environ.get("PORT", 5000))  # For deployment to Heroku
        app.run(host='0.0.0.0', port=port)  # When deployed locally, used port 9696
    else:
        app.run(debug = True, host = '0.0.0.0', port = 9696)

