from flask import Flask
from flask import jsonify
#import trainermodel as tr
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
model=pickle.load(open('model.pkl','rb'))
encoder=LabelEncoder()
d1= pd.read_csv('training.csv')
y=d1.iloc[:,-1:]
y['prognosis']=encoder.fit_transform(y['prognosis'])
code_value=y['prognosis'].unique()
name_value=(d1['prognosis'].unique())
name_value=sorted(name_value)

m=[x  for x in range(len(name_value))]
name_maper={m[i]:name_value[i] for i in range(len(name_value))}
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"
@app.route('/[0,0,0,6]/')
def success():
    return ('You have perfectly typed [0,0,0,6]')


@app.route('/predict/<inputs>')
def show_post(inputs):
    inputs=str(inputs)
    inputs=inputs.split('_')
    
    X=d1.iloc[:,:-1]
    symptoms = X.columns.values
    symptom_index={}
    for index, value in enumerate(symptoms):
        symptom = value
        symptom_index[index] = value
    
    data_dict = {
        
        "predictions_classes":LogisticRegression.encoder.classes_,
        "symptom_index":symptom_index
    }
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in inputs:
        index = int(symptom)
        input_data[index] = 1
        
    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1,-1)
    final_pred=model.predict(input_data)[0]
    return jsonify(code=str(final_pred),
    name=name_maper[final_pred]
    )   


    
    
    


    
    
    #use post title to fetch the record from db
@app.route('/numbers/')
def print_list():
    return jsonify(list(range(5)))    
if __name__ == '__main__':
    app.run()
