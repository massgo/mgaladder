#! /usr/bin/env python3

# Flask server for MGA ladder

from flask import Flask, jsonify

from models import Player
from models import Result

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    """ serves static file for testing purposes"""
    return app.send_static_file('index.html') 

@app.route('/results')
def results():
    resultsList = {"results": [
        {"black": "Walther", "white": "Andrew"},
        {"black": "Walther", "white": "Chun"}
        ]}
    return jsonify(resultsList)

if __name__ == '__main__':
    app.run(debug=True)
