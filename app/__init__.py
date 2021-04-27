from flask import Flask, render_template, session, request
from uuid import uuid4
from helpers import a_clean
from time import localtime, strftime
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
    return render_template("root.html")

def error():
    return render_template("error.html")


'''
logout function
'''
@app.route("/logout")
def logout():
    try:    
        if session.get('user_id'): # if user logged in 
            session.pop('user_id') # clear all
            session.pop('username')
        return root()
    except:
        return render_template("error.html")


@app.route("/user_page")
def user_page():
    curr_time = strftime("%H:%M:%S", localtime())
    hour_time = int(curr_time[:2])
    message_time = 0

    if hour_time >= 12 and hour_time <= 18:
        message_time = 1
    
    if hour_time > 18:
        message_time = 2
        
    # TODO: RETRIEVE NOTE FROM DB
    greetings = ["Good morning", "Good afternoon", "Good evening"]
    for greeting in greetings:
        greeting += ", " + session.get("username")
    return render_template("user_page.html", greeting=greetings[message_time])


'''
login function
'''
@app.route("/login", methods=["POST"])
def login():
    # based on form, have form.request['elem'] tags here
    username = request.form["username"]
    password = request.form["password"]

    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()
    c.execute(f"SELECT password, user_id FROM users WHERE username = '{username}'")
    accounts = list(c) #returns tuple
    if len(accounts) != 1:
        return error()
    elif password != accounts[0][0]:
        return error() # wrong password - js error for that
    else:
        session['username'] = username # add user and user_id to session for auth purposes
        session['user_id'] = accounts[0][1]
    return user_page()
    

'''
register function, registers new users
'''
@app.route("/register", methods=["POST"])
def register():
    #TODO INCLUDE TRY-CATCH BLOCKS FOR EACH FUNCTION
    username = request.form["username"]
    password = request.form["password"]

    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()
    c.execute("SELECT username FROM users")

    pre_existing_usernames = list(c)

    if (username) in pre_existing_usernames:
        return # TODO render_template() # return "user already exists js error"
    else:
        user_id = uuid4() # generate new uuid for user
        c.execute(f"INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)", (user_id, username, password))
        session['username'] = str(username)
        session['user_id'] = user_id
        db.commit()
        return user_page()
    return root()



@app.route("/notes_update")
def update_note():
    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()

    content = a_clean(request.form["notes"])

    c.execute("") #TODO DELTE OLD NOTE
    # TODO EXECUTE WITH NEW NOTE CONTENT AS BODY

    return user_page()


if __name__ == '__main__':
    app.debug = True
    app.run()