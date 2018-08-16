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
    if "username" in session:
        if session["account"] == "donor":
            items = db_stuff.get_all_item_info()
            return render_template("home.html", items = items)
        if session["account"] == "admin":
            return render_templaet("admin_home.html")
    else:
        return render_template("login.html")

#    return "Hello World"

@app.route('/admin')
def admin():
    if "username" in session and session["account"] == "admin":
        return render_remplate("admin_home.html")
    else:
        return render_template("admin_login.html")



@app.route('/admin_auth', methods=["GET","POST"])
def admin_auth():
    if "username" in session and session["account"] == "admin":
        return render_template("admin_home.html")
    try: 
        username = request.form["username"]
        print username
        password = request.form["password"]
        print password
        
    except KeyError:
        return render_template("admin_login.html", error="please fill everything in")
    
    if db_stuff.admin_auth(username, password):
        session["username"] = username
        session["account"] = "admin"
        print "Success!"
        return render_template("admin_home.html")
    
    else:
        return render_template("admin_login.html")




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
        print "running try"
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
        items = db_stuff.get_all_item_info()
        return render_template("home.html", items = items)
    else:
        #flash("Login failed. Please try again.")
        return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if "username" in session:
        if session["account"] == "donor":
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    if request.method == "GET":
        return render_template("login.html")
    try:
        fname = request.form["fname"]
        lname = request.form["lname"]
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
    except KeyError:
        #flash('fill everything in please')
        print 'key error'
        return render_template("signup.html")
    if db_stuff.add_donor(fname, lname, username, password, email):
        flash("successfully added donor!")
        return render_template("home.html")
    else:
#        flash("failed to add donor")
        return render_template("login.html")


@app.route('/home')
def home():
    return render_template('home.html', item=[{'price':'$2.50', 'name':'emacs', 'id':7,'desc':'its worth that little'}, {'price':'$5.00', 'name':'atom', 'id':8,'desc':'its worth way more'}])


@app.route('/admin_home')
def admin_home():
    if "username" in session and session["account"] == "admin":
        render_template("admin_home.html")
    else:
        render_template("admin_login.html")

@app.route('/logout')
def logout():
    if "username" in session:
        session.pop("username")
        session.pop("account")
    return redirect(url_for('root'))


app.secret_key = os.urandom(32)
if __name__ == '__main__':
    #app.secret_key = os.urandom(32)
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
