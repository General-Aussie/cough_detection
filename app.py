#!/usr/local/bin/python3.7

from flask import Flask, render_template, make_response, request, jsonify, redirect, url_for, session, abort, \
    send_from_directory
import os
import librosa
import numpy as np
import tensorflow as tf
from numpy import argmax
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.debug = True

def feature_extract(file):
    audio, sr = librosa.load(file, res_type='kaiser_fast')
    mfccs_feature = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfccs_scaled_feature = np.mean(mfccs_feature.T, axis=0)
    return mfccs_scaled_feature


# get the absolute path to the my_model.h5 file
model_path = os.path.abspath('respir_model.h5')
print(model_path)
# load the saved model
loaded_model = load_model(
    model_path, compile=False)


def ANN_predict(file_name, predict_demo_fac):
    predict_data = feature_extract(file_name)
    # 'age','gender','respiratory_condition','fever_muscle_pain' order
    predict_concat = np.concatenate((predict_data, predict_demo_fac), axis=0)
    input = predict_concat
    input_array = np.asarray(input)
    input_reshaped = input_array.reshape(1, -1)
    input_reshaped.shape
    cough_res = None
    # print("  Covid-19   Healthy   Symptomatic")
    cough_res = loaded_model.predict(input_reshaped)
    return cough_res

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/home', methods=['POST', 'GET'])
def respir():
    result = None
    predicts = None
    uploaded_data = []
    if request.method == 'POST':
        # Get the selected parameters
        age = int(request.form.get('param1', 0))
        fever_musclePain = int(request.form.get('param2', 0))
        gender = int(request.form.get('gender', 0))
        respiratory_condition = int(request.form.get('param4', 0))
        # Get the uploaded audio file
        audio_file = request.files['audio_file']
        if gender == 2:
            # female
            gender = 0
        # male
        elif gender == 1:
            gender = 1
        else:
            gender = None
        # Save the audio file to disk
        audio_file_path = os.path.join('uploads', audio_file.filename)
        audio_file.save(audio_file_path)
        rees = [age, respiratory_condition, fever_musclePain, gender]
        print(rees)
        print(audio_file_path)
        for i in rees:
            uploaded_data.append(i)
        print(uploaded_data)
        if uploaded_data and audio_file_path:
            print("good")
            predicts = ANN_predict(audio_file_path, uploaded_data)
            print(predicts)
            max_index = None
            max_index = np.argmax(predicts)
            print(max_index)
            if max_index == 0:
                result = "Covid-19"
            elif max_index == 1:
                result = "Healthy"
            else:
                result = "Symptomatic"
        # return the result as a JSON object
        response = make_response({'result': result})
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        return render_template('index.html')   

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
