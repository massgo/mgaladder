#! /usr/bin/env python3

# Flask server for MGA ladder

from flask import Flask, jsonify

from models import Player, Result, Ladder, Standing

app = Flask(__name__, static_url_path='')


ladders = Ladder.select()

if len(ladders) == 0:
  ladder = Ladder(name="default")
  ladder.save()
else:
  ladder = ladders[0]


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

# list players with their position in the ladder
# create player
# add player to ladder
# remove from ladder
# add game result

if __name__ == '__main__':
    app.run(debug=True)
