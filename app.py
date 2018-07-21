from flask import Flask, redirect, url_for,render_template, session, request, flash
import os
from os import path
import sqlite3
import hashlib
#import db_stuff

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def root():
    if "username" in session:
        if session["account"] == "donor":
            return render_template("home.html")
        if session["account"] == "admin":
            return render_templaet("admin_home.html")
    else:
        return render_template("login.html")

#    return "Hello World"

@app.route('/auth', methods=["GET", "POST"])
def auth():
    print "running auth"
    if "username" in session:
        if session["account"] == "donor":
            return render_template("home.html")
        if session["account"] == "admin":
            return render_templaet("admin_home.html")
    if request.method == "GET":
        return redirect("/")
    try:
        username = request.form['username']
        print username
        password = request.form['password']
        print password
    
    except KeyError:
        #flash("please fill everything in")
        return render_template("login.html", error="please fill everything in")

    if db_stuff.auth(username, password):
        session["username"] = username
        session["account"] = "donor"
        print "Success!"
        #flash("You're logged in!")
        return render_template("home.html")
    else:
        #flash("Login failed. Please try again.")
        return render_template("login.html")


app.secret_key = os.urandom(32)
if __name__ == '__main__':
    #app.secret_key = os.urandom(32)
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
