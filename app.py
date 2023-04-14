#!/usr/local/bin/python3.7

from flask import Flask, render_template, make_response, request, jsonify, redirect, url_for, session, abort, \
    send_from_directory
import os


app = Flask(__name__)
app.debug = True


@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)
