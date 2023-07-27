#!/usr/bin/python

from flask import Flask, render_template, jsonify, session
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    username=""
    if "username" in session:
        username=session["username"]

    return render_template(
            "index.html",
            username=username
    )

@app.route("/w/login")
def login():
    if "username" in session:
        return render_template(
            "hello.html",
            username=session["username"]
        )
    else:
        return render_template("login.html")

@app.route("/w/loginfail")
def loginfail():
    if "username" in session:
        return redirect("/w/login", code=302)
    else:
        return render_template("loginfail.html")

@app.route("/w/signup")
def signup():
    return render_template("signup.html")
     

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9000,
        debug=False
    )
