import os
import uuid

from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
user_info = "user_info"
user_account = "user_account"


@app.route("/")
def home():
    return render_template("templates/main/index.html")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
