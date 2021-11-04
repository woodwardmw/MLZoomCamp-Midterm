import pandas as pd
import random
import requests


df = pd.read_csv('data/vowels_data.csv')

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

df.drop(columns = "train_test", inplace = True)

df_test = df[df.speaker.isin([10, 11, 13, 14])]  # Two male and two female in df_test

random_index = random.randint(0, df_test.shape[0] - 1)

example = df_test.drop(['speaker', 'vowel'], axis=1).iloc[[random_index,]]
example = example.to_dict()
vowel_int = df_test.iloc[random_index]['vowel'].astype(int)
print(f'Actual vowel: {convert_to_vowel(vowel_int)}')

url = 'https://zoomcamp-midterm-heroku.herokuapp.com/predict'
response = requests.post(url, json=example)
result = response.json()
print(f'Predicted vowel: {result["Prediction"]}')