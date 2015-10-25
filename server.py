#! /usr/bin/env python3

# Flask server for MGA ladder

from flask import Flask, jsonify, request, m

from models import Player, Result

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    """ serves static file for testing purposes"""
    return app.send_static_file('index.html') 

# list all players
@app.route('/players', method=['GET'])
def players():
    players = Player.select()
    return jsonify(Player.players(players))

@app.route('/players/<id>', method=['DELETE'])
def players(id):
    player = Player.get(id=id)
    player.delete_instance()
    return ('', 204)

@app.route('/players', method=['POST'])
def players():
    data = request.get_json()
    player = Player(data)
    player.save()
    return jsonify(dict(player))

@app.route('/standings')
def standings():
    players = Player.select().where(Player.active==True)
    return jsonify(Player.players(players))

@app.route('/drop/<id>')
def drop(id):
    player = Player.get(id=id)
    player.drop()
    player.save()
    return ('', 204)

@app.route('/result', method=['POST'])
def result():
    data = request.get_json()
    result = Result(data)
    result.save()
    return ('', 204)


# create player
# remove from ladder
# remove from db
# add game result

if __name__ == '__main__':
    app.run(debug=True)
