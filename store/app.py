#!/usr/bin/python

from flask import Flask, jsonify 
import json
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
@app.route("/api/store/<id>", methods=["GET"])
def store(id):
    store_status={"100":0, "101":1, "102":1, "103":1 "104":1 "105":1 "106":0 "107":1}
    if id in  store_status.keys():
        data={"status": store_status[id]}
        return jsonify(data) 
    else:
        data={"status": -1}
        return jsonify(data) 

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9003,
        debug=True
    )

