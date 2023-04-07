from flask import Flask, render_template, request, jsonify, redirect, url_for, session, abort, \
    send_from_directory
import os
import librosa
import pandas as pd
import numpy as np
import tensorflow as tf
#from tensorflow.keras.model import load_model

app = Flask(__name__)
app.debug = True

@app.route('/home')
def forgot():
	return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_audio():
	if request.method == 'POST':
		# Get the selected parameters
		age = request.form['param1']
		fever_musclePain = request.form['param2']
		gender = request.form['gender']
		respiratory_condition = request.form['param4']
		# Get the uploaded audio file
		audio_file = request.files['audio_file']

	# Save the audio file to disk
	audio_file.save(os.path.join('upload', audio_file.filename))

	# return the uploaded audio file and parameters
	return 'Audio uploaded successfully!', age,fever_musclePain, gender

def feature_extract(file):
    audio,sr=librosa.load(file_name,res_type='kaiser_fast')
    mfccs_feature=librosa.feature.mfcc(y=audio,sr=sr,n_mfcc=40)
    mfccs_scaled_feature=np.mean(mfccs_feature.T,axis=0)
    return mfccs_scaled_feature

# load the saved model
loaded_model = tf.keras.models.load_model('my_model.h5 ', compile = False)

def ANN_predict(file_name,predict_demo_fac):
    predict_data=feature_extract(file_name)
    #'age','gender','respiratory_condition','fever_muscle_pain' order
    predict_concat=np.concatenate((predict_data, predict_demo_fac), axis=0)
    input=predict_concat
    input_array=np.asarray(input)
    input_reshaped=input_array.reshape(1,-1)
    input_reshaped.shape
    print("  Covid-19   Healthy   Symptomatic")
    print(loaded_model.predict(input_reshaped))


file_name='/Users/mac/Downloads/00039425-7f3a-42aa-ac13-834aaa2b6b92.webm'
predict_demo_fac=[19,1,0,0]
ANN_predict(file_name,predict_demo_fac)



if __name__ == '__main__':
	app.run()
