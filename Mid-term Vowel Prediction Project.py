#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import sklearn
pd.set_option('display.max_rows', 200)
from statistics import mean
from sklearn.feature_selection import mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import pickle 
import requests



df = pd.read_csv('vowels_data.csv')
df

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

df_train = df[df.speaker.isin([0,1,2,3,4,5,6,7,8,9,12])]
df_train = df_train.sample(frac=1).reset_index(drop=True)  # Randomise the order of the training examples

df_train.head()

df_train.dtypes

df_train.isnull().sum()

sns.boxplot(data = df_train[['f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9']])

MI = mutual_info_classif(df_train.drop(['vowel', 'speaker'], axis=1), df_train['vowel'])

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(df_train.drop(['vowel', 'speaker'], axis=1).columns, MI)
plt.show()

def evaluate_model(model, df_train = df_train):
    speakers = df_train['speaker'].unique()
    scores = []
    accuracy = []
    for speaker in speakers:
        df_train = df_train.copy()
        X_train = df_train[df_train['speaker'] != speaker]
        X_val = df_train[df_train['speaker'] == speaker]
        y_train = df_train.loc[df_train['speaker'] != speaker]['vowel']
        y_val = df_train.loc[df_train['speaker'] == speaker]['vowel']
        model.fit(X_train.drop(['vowel', 'speaker'], axis=1), y_train)
        y_preds_proba = model.predict_proba(X_val.drop(['vowel', 'speaker'], axis=1))
        y_preds = model.predict(X_val.drop(['vowel', 'speaker'], axis=1))
        scores.append(roc_auc_score(y_val, y_preds_proba, multi_class='ovo'))
        accuracy.append(mean((y_preds == y_val).astype(int)))
    return mean(scores), mean(accuracy)

lr = LogisticRegression(multi_class="multinomial", solver='saga')
AUC, accuracy = evaluate_model(lr)
print(f'AUC: {AUC}\nAccuracy: {accuracy}')

rf = RandomForestClassifier()
AUC, accuracy = evaluate_model(rf)
print(f'AUC: {AUC}\nAccuracy: {accuracy}')

gb = GradientBoostingClassifier()
AUC, accuracy = evaluate_model(gb)
print(f'AUC: {AUC}\nAccuracy: {accuracy}')

n_estimators_list = [25, 50, 100, 200, 400, 800, 1600]

for n in n_estimators_list:
    rf = RandomForestClassifier(n_estimators=n)
    print(f'n_estimators: {n} \t AUC: {evaluate_model(rf)}')

n_estimators_list = [300, 400, 500, 600, 800, 1200, 1600]

for n in n_estimators_list:
    rf = RandomForestClassifier(n_estimators=n)
    print(f'n_estimators: {n} \t AUC: {evaluate_model(rf)}')

max_depth_list = [10, 15, 20, 30, 50]

for m in max_depth_list:
    rf = RandomForestClassifier(n_estimators=500, max_depth=m)
    print(f'max_depth: {m} \t AUC: {evaluate_model(rf)}')

max_depth_list_short = [10, 15, 20]
n_estimators_list_short = [400, 500, 600, 800]

for m in max_depth_list_short:
    for n in n_estimators_list_short:
        rf = RandomForestClassifier(n_estimators=n, max_depth=m)
        print(f'max_depth: {m}, n_estimators: {n} \t AUC, Accuracy: {evaluate_model(rf)}')

rf = RandomForestClassifier(n_estimators=800, max_depth=15)
AUC, accuracy = evaluate_model(rf)
print(f'AUC: {AUC}\nAccuracy: {accuracy}')

model = RandomForestClassifier(n_estimators=800, max_depth=15)
model.fit(df_train.drop(['vowel', 'speaker'], axis=1), df_train['vowel'])

with open('vowel-model.bin', 'wb') as f_out:
    pickle.dump((model), f_out)

random_index = random.randint(0, df_test.shape[0] - 1)

example = df_test.drop(['speaker', 'vowel'], axis=1).iloc[[random_index,]]
example = example.to_dict()
vowel_int = df_test.iloc[random_index]['vowel'].astype(int)
print(f'Actual vowel: {convert_to_vowel(vowel_int)}')

vowel_int = model.predict(df_test.drop(['speaker', 'vowel'], axis=1).iloc[[random_index,]])[0]
print(f'Predicted vowel: {convert_to_vowel(vowel_int)}')

# import requests
# url = 'http://localhost:9696/predict'
# response = requests.post(url, json=example)
# result = response.json()
# result


# This example, predicted from the remotely run Docker file on Heroku:

url = 'https://zoomcamp-midterm-heroku.herokuapp.com/predict'
response = requests.post(url, json=example)
result = response.json()
print(result)