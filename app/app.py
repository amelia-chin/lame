from flask import Flask, render_template, session, request
from uuid import uuid4
import datetime             # how to get current date / time
import sqlite3
import os
import sys

app = Flask(__name__)
app.secret_key = os.urandom(32)
dir = os.path.dirname(__file__) or "."
dir += "/"


'''
root landing page
'''
@app.route("/")
def root():
    return "Hello world!"

'''
login function
'''
@app.route("/login")
def login():
    # based on form, have form.request['elem'] tags here
    username = ""
    password = ""

    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()
    c.execute(f"SELECT password, user_id FROM users WHERE username = '{username}'")
    accounts = list(u) #returns tuple
    if len(accounts) != 1:
        return render_template() # login failed
    elif password != accounts[0][0]:
        return render_template() # wrong password - js error for that
    else:
        session['username'] = username # add user and user_id to session for auth purposes
        session['user_id'] = accounts[0][1]
    
'''
register function, registers new users
'''
@app.route("/register")
def register():
    try:
        db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
        c = db.cursor()
        c.execute("SELECT username FROM users")
        pre_existing_usernames = list(u)
        if (username) in pre_existing_usernames:
            return render_template() # return "user already exists js error"
        else:
            user_id = uuid4() # generate new uuid for user
            u.execute(f"INSERT INTO users(user_id, username, password) VALUES ('{user_id}','{username}','{password}')")
            session['username'] = str(username)
            session['user_id'] = user_id
            db.commit()
    except:
        return # we should make an "oops! there was an error page to prevent the thing from ever crashing"


if __name__ == '__main__':
    app.debug = True
    app.run()