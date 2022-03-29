from dao import Dao
from flask import Flask, jsonify, request, render_template
from util import get_approximate_datetime

app = Flask(__name__, static_folder = "../dist/static", template_folder = "../dist")
dao = Dao()

@app.route("/room")
def search_room():
    return jsonify(dao.search_room(request.args.get('keyword')))

@app.route("/medalnames")
def list_medal_names():
    return jsonify(dao.list_medal_names(request.args.get('roomid')))

@app.route("/medallevels")
def list_medal_levels():
    return jsonify(dao.list_medal_levels(request.args.get('roomid'), request.args.get('medalid')))

@app.route("/datetime")
def last_update_datetime():
    return jsonify(f"{get_approximate_datetime():%Y-%m-%d %H:%M:%S}")

@app.route('/')
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)