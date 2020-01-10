import sys
import sqlite3
import os
import hashlib

from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm
from extraction.model.train import ModelTrainer

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Markup, session

from contextlib import closing

import json

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

# App routes
# example select
#    cur = g.db.execute('Select * from Corpus')
#    rows = cur.fetchall()
# example insert
#    cur = g.db.execute('Insert Into Corpus (EntityType, RawText) Values (1, "Test Text")')
#    g.db.commit()

@app.route("/")
def index():
    cur = g.db.execute('Select * from Model')
    rows = cur.fetchall()
    print(rows)
    return render_template("index.html", models=rows)


@app.route("/model/<int:id>")
def get_model(id):
    cur = g.db.execute("Select * from Model where id = '" + str(id) + "'")
    model = cur.fetchall()[0]
    model_dict = {}
    model_dict["description"] = model[2]
    return json.dumps(model_dict)


@app.route("/select-model", methods=['POST', 'GET'])
def select_model():
    if request.method == 'POST':
        result = request.form.get("model-select")
        cur = g.db.execute('Select * from Model where id = ' + result).fetchall()[0]
        session["selected_model_id"] = str(cur[0])
        session["selected_model"] = str(cur[1])
        return render_template("input.html")
    elif request.method == 'GET':
        return render_template("input.html")

@app.route("/output", methods=['POST', 'GET'])
def output():
    if request.method == 'POST':
        results = request.form['input-text']
        row = session['selected_model_id']
        cur = g.db.execute("SELECT GroupName, BackendName FROM Model WHERE id = " + row)
        t = cur.fetchall()
        model = ExtractionModel(t[0][0], t[0][1])
        i = model.extract(results)
        new_dict={}
        for key, value in i.items():
            new_dict[key] = value.replace('B-', '').replace('I-', '').replace('O-', '')

        text,mp = get_extraction_colors(new_dict, results.split(" "))
        tags = get_category_colors(i.values())
        color_set = ["#004c97", "#ff9e15", "#a5cd50", "#2dbecd", "#e61e50", "#007944, #fff, #111"]
        return render_template("output2.html", extraction=text, tags=tags, original_word_set=results.split(" "), color_set=mp)
    elif request.method == 'GET':
        return render_template("output.html", input_text=None)


def get_category_colors(tags):
    color_set = ["#004c97", "#ff9e15", "#a5cd50", "#2dbecd", "#e61e50", "#007944","#fff","#111"]
    tags = [tag.replace('B-', '').replace('I-', '').replace('O-', '') for tag in tags]
    return list(set(tags))


def search_color(search_tag,color_map):
    tags = [tag for tag,color in color_map]
    colors = [color for tag,color in color_map]
    tag_idx = tags.index(search_tag)
    if tag_idx != -1:
        return colors[tag_idx]

def get_extraction_colors(extraction, orig):
    print("original:", orig)
    color_set = ["#004c97", "#ff9e15", "#a5cd50", "#2dbecd", "#e61e50", "#007944","#fff","#111"]
    curr_extraction = extraction[list(extraction.keys())[0]]
    color_map = []
    seen_tags = [extraction[list(extraction.keys())[0]]]
    color_map.append((list(extraction.values())[0], color_set[0]))
    i = 0
    wc = 0
    final_string = "<mark>"
    for word, tag in extraction.items():
       # print(curr_extraction, curr_extraction == tag, word, tag)
        if word == "xxxPADDINGxxx":
            if(wc >= len(orig)):
                word = ""
            else: 
                word = orig[wc]

        if curr_extraction == tag:
            clr = search_color(tag, color_map)
            final_string += "<span style='color: {}'>{}</span> ".format(clr, word)
        else:
            final_string += "</mark>&nbsp;"

            if tag not in seen_tags:
                i+=1
                color_map.append((tag, color_set[i]))

            print(i, len(color_set))
            seen_tags.append(tag)
            clr = search_color(tag, color_map)
            final_string += "<mark><span style='color: {}'>{}</span> ".format(clr, word)
            curr_extraction = tag 
        wc+=1
    return (final_string, color_map)
            
        
    #tags = [tag.replace('B-', '').replace('I-', '').replace('O-', '') for tag in tags]
    #return list(set(tags))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
