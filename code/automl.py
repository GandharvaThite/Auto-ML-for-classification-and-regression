# -*- coding: utf-8 -*-
"""AutoML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VLNJyErVatSj_TXmatt4KL8kBWUk38qo
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split,GridSearchCV,RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor


df = pd.read_csv('/data/Copy of sonar data.csv',header = None)

df = df.drop(0)

"""## **Identification of type of dataset using Gandharva's Constant**"""

type_of_dataset = None
r = df.shape
last_ind = r[1]-1
total_entries = r[0]-1
set_contents = set(df[last_ind])
gandharva_constant = len(set_contents)/total_entries
if(gandharva_constant>=0.4):
  type_of_dataset = 'regression'
else:
  type_of_dataset = 'classification'
print(type_of_dataset)

"""# **Now splitting the dataset**"""



X = (df.drop(columns = last_ind,axis = 1))
Y = np.asarray(df[last_ind])
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 0.2,random_state = 1)

"""# **Input values for prediction**"""

input_data = (0.0139,0.0222,0.0089,0.0108,0.0215,0.0136,0.0659,0.0954,0.0786,0.1015,0.1261,0.0828,0.0493,0.0848,0.1514,0.1396,0.1066,0.1923,0.2991,0.3247,0.3797,0.5658,0.7483,0.8757,0.9048,0.7511,0.6858,0.7043,0.5864,0.3773,0.2206,0.2628,0.2672,0.2907,0.1982,0.2288,0.3186,0.2871,0.2921,0.2806,0.2682,0.2112,0.1513,0.1789,0.1850,0.1717,0.0898,0.0656,0.0445,0.0110,0.0024,0.0062,0.0072,0.0113,0.0012,0.0022,0.0025,0.0059,0.0039,0.0048)

# input_data = (4)

"""# **If dataset is Classification**"""


if(type_of_dataset == 'classification'):
  algo_names = ['svm','random_forest','logistic_regression','decision_tree']
  algo = [svm.SVC(),RandomForestClassifier(),LogisticRegression(),tree.DecisionTreeClassifier()]
  model_params = {
   'svm':{
   'model':svm.SVC(gamma='auto'),
   'params':{
       'C':[1,10,20],
       'kernel':['linear','poly','rbf']

   }
  } ,
  'random_forest':{
       'model':RandomForestClassifier(),
       'params':{
           'n_estimators':[1,5,10,50,100,150,500,1000]
       }
   },
   'logistic_regression':{
       'model':LogisticRegression(solver = 'liblinear',multi_class='auto'),
       'params':{
          'C':[1,5,10,50,100,150,500,1000]
       }
   },
   'decision_tree':{
       'model':tree.DecisionTreeClassifier(),
       'params':{
           'criterion':['gini','entropy','log_loss'],
           'splitter':['best','random']
       }
   },
    }
  scores = []
  for model_name,mp in model_params.items():
    clf = GridSearchCV(mp['model'],mp['params'],cv =5,return_train_score=False)
    clf.fit(X_train,Y_train)
    scores.append({
      'model_name':model_name,
      'best_score':clf.best_score_,
      'best_parameters':clf.best_params_
    }
    )
  a = []
  b = []
  final_scores = list(scores)
  for i in range(len(final_scores)):
    a.append(list(final_scores[i].values()))
  for i in range(len(a)):
    b.append(a[i][1])
  maxi_ind = -1
  for i in range(len(b)):
    if(b[i] == max(b)):
      maxi_ind = i
      break
  model = algo[maxi_ind]
  model.fit(X_train,Y_train)
  X_test_prediction = model.predict(X_test)
  ml_final_result_accuracy = accuracy_score(X_test_prediction,Y_test)
  
  input_data_as_np_array = np.asarray(input_data)
  input_data_reshaped = input_data_as_np_array.reshape(1,-1)
  prediction = model.predict(input_data_reshaped)

print(prediction[0])

# Report Printing
if(type_of_dataset == 'classification'):
  arr = ['Model: ','Accuracy: ', 'Parameters Tuned: ']
  print("********************* Report ***********************************")
  print()
  print("Prediction for your values: ",prediction[0])
  print("Type of dataset: ",type_of_dataset)
  for i in range(len(a[maxi_ind])):
    print(arr[i],a[maxi_ind][i])
  print()
  print("****************************************************************")

"""# **If dataset is Regression**"""



if(type_of_dataset == 'regression'):
  algo_names = ['Linear Regression','CGBoost Regressor']
  algo = [LinearRegression(),GradientBoostingRegressor()]
  model_params = {
      'linear_regression':{
   'model':LinearRegression(),
   'params':{
      #  'fit_intercept': 1
   }
  } ,
  'random_forest':{
       'model':GradientBoostingRegressor(),
       'params':{
           'n_estimators':[1,5,10,50,100,150,500,1000],
           "learning_rate": [0.01,0.1,0.5]
       }
   },
  }
  scores = []
  for model_name,mp in model_params.items():
    clf = GridSearchCV(mp['model'],mp['params'],cv =5,return_train_score=False)
    clf.fit(X_train,Y_train)
    scores.append({
      'model_name':model_name,
      'best_score':clf.best_score_,
      'best_parameters':clf.best_params_
    }
    )
  a = []
  b = []
  final_scores = list(scores)
  for i in range(len(final_scores)):
    a.append(list(final_scores[i].values()))
  for i in range(len(a)):
    b.append(a[i][1])
  maxi_ind = -1
  for i in range(len(b)):
    if(b[i] == max(b)):
      maxi_ind = i
      break
  model = algo[maxi_ind]
  model.fit(X_train,Y_train)
  X_test_prediction = model.predict(X_test)
  # ml_final_result_accuracy = accuracy_score(X_test_prediction,Y_test)
  input_data_as_np_array = np.asarray(input_data)
  input_data_reshaped = input_data_as_np_array.reshape(1,-1)
  prediction = model.predict(input_data_reshaped)

print(prediction)

# Report Printing
if(type_of_dataset == 'regression'):
  arr = ['Model: ','Accuracy: ', 'Parameters Tuned: ']
  print("********************* Report ***********************************")
  print()
  print("Prediction for your values: ",prediction[0])
  print("Type of dataset: ",type_of_dataset)
  for i in range(len(a[maxi_ind])):
    print(arr[i],a[maxi_ind][i])
  print()
  print("****************************************************************")
