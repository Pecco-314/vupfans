from dao import Dao
from flask import Flask, jsonify, request

app = Flask(__name__)
dao = Dao()

@app.route("/room")
def search_room():
    return jsonify(dao.search_room(request.args.get('keyword')))

@app.route("/medalnames")
def list_medal_names():
    return jsonify(dao.list_medal_names(request.args.get('roomid')))

@app.route("/medallevels")
def list_medal_levels():
    return jsonify(dao.list_medal_levels(request.args.get('roomid'), request.args.get('medalname')))