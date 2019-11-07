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

@app.route("/")
def index():
    return render_template("input.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
