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

print(models)

"""
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db #


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
"""

#App routes

@app.route("/")
def index():
    return render_template("index.html", models=models)

@app.route('/input')
def input():
    return render_template("input.html")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
