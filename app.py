#!/usr/local/bin/python3.7

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, abort, \
    send_from_directory
import os
import librosa
import pandas as pd
import numpy as np
import tensorflow as tf
from numpy import argmax
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.debug = True

@app.route('/home')
def forgot():
    return render_template("index.html")

def feature_extract(file):
    audio, sr = librosa.load(file, res_type='kaiser_fast')
    mfccs_feature = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfccs_scaled_feature = np.mean(mfccs_feature.T, axis=0)
    return mfccs_scaled_feature


# load the saved model
loaded_model = tf.keras.models.load_model(
    'my_model.h5', compile=False)


def ANN_predict(file_name, predict_demo_fac):
    predict_data = feature_extract(file_name)
    # 'age','gender','respiratory_condition','fever_muscle_pain' order
    predict_concat = np.concatenate((predict_data, predict_demo_fac), axis=0)
    input = predict_concat
    input_array = np.asarray(input)
    input_reshaped = input_array.reshape(1, -1)
    input_reshaped.shape
    # print("  Covid-19   Healthy   Symptomatic")
    cough_res = loaded_model.predict(input_reshaped)
    return cough_res


@app.route('/upload', methods=['POST'])
def upload_audio():
    result = ''
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
        for i in rees:
            uploaded_data.append(i)
        if uploaded_data and audio_file:
            predicts = ANN_predict(audio_file_path, uploaded_data)
            result = None
            max_index = np.argmax(predicts)
            if max_index == 0:
                result = "Covid-19"
            elif max_index == 1:
                result = "Healthy"
            else:
                result = "Symptomatic"
    
    # return the uploaded audio file and parameters
    print(rees)
    print(result, max_index)
    print(predicts)
    return render_template('index.html', result=result)
    



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
