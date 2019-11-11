import sys
import sqlite3
import os
import hashlib

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Markup

from contextlib import closing

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(__name__)

# Set up sqlite database

conn = sqlite3.connect('nlp4nm.db')
c = conn.cursor()

c.execute('SELECT {cn} FROM {tn}'.\
        format(tn='model', cn='ModelName'))
models = c.fetchall()

# App routes


@app.route("/")
def index():
    return render_template("index.html", models=models)


@app.route("/input", methods=['POST', 'GET'])
def input():
    if request.method == 'POST':
        result = request.form
        return render_template("input.html", result=result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
