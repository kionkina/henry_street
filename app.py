from flask import Flask, redirect, url_for,render_template, session, request, flash
import os
from os import path
import sqlite3
import hashlib
import db_stuff

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def root():
    return "Hello World"

app.secret_key = os.urandom(32)
if __name__ == '__main__':
    #app.secret_key = os.urandom(32)
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
