import sys
import sqlite3
import os
import hashlib

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Markup, session

from contextlib import closing

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(__name__)

DATABASE = 'nlp4nm.db'
DEBUG = True
SECRET_KEY = "shoeball"
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(__name__)


# Database setup
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('db/schema/db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exection):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def not_found_error(e):
    return render_template('./response/404.html')


@app.errorhandler(500)
def bad_code_error(e):
    return render_template('./response/500.html')

# Set up sqlite database

conn = sqlite3.connect('nlp4nm.db')
c = conn.cursor()


c.execute('SELECT {cn} FROM {tn}'.\
          format(tn='model', cn='ModelName'))
models = c.fetchall()

# App routes


@app.route("/")
def index():

# example select
#    cur = g.db.execute('Select * from Corpus')
#    rows = cur.fetchall()
# example insert
#    cur = g.db.execute('Insert Into Corpus (EntityType, RawText) Values (1, "Test Text")')
#    g.db.commit()

    cur = g.db.execute('Select * from Model')
    rows = cur.fetchall()
    return render_template("index.html", models=rows)
    return render_template("index.html", models=models)



@app.route("/input", methods=['POST', 'GET'])
def input():
    if request.method == 'POST':
        result = request.form.get("model-select")
        selected_model = str(result)
        session["selected_model"] = selected_model
        return render_template("input.html", selected=selected_model)
    elif request.method == 'GET':
        return render_template("input.html", result=None)

@app.route("/output", methods=['POST', 'GET'])
def output():
    
    return render_template("output.html", result=None)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)

