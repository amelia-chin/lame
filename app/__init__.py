from flask import Flask, render_template, session, request
from uuid import uuid4
from helpers import a_clean, get_greeting, tup_clean, a_remove, convert
from time import localtime, strftime

import datetime             # how to get current date / time
import sqlite3
import os
import sys
import urllib
import json

app = Flask(__name__)
app.secret_key = os.urandom(32)
dir = os.path.dirname(__file__) or "."
dir += "/"


# TODO: include try/catch blocks for each function
## To-do list functionality (all)
## error handling for if a username / password already exists


def random_error():
    return render_template("error.html", message="Something went wrong.", route="/")


'''
root landing page
'''
@app.route("/", methods=["POST", "GET"])
def root():
    try:
        if session.get("username"):
            return user_page()
        return render_template("login.html")
    except:
        return random_error()

'''
logout function
'''
@app.route("/logout")
def logout():
    try:
        if session.get('user_id'): # if user logged in
            # TODO: can we find a way to have the notes section save on logout? would require we
            ## run the actual form from the HTML file
            session.pop('user_id') # clear all
            session.pop('username')
        return root()
    except:
        return render_template("error.html") #TO DO: add error message


def auth_error(is_user_conflict=False, is_login_incorrect=False):
    if is_user_conflict:
        return render_template("register.html", message="Username Already Exists.")
    if is_login_incorrect:
        return render_template("login.html", message="Username or Password is Incorrect.")


'''
all content contained on main user page within this function
'''
@app.route("/user_page")
def user_page():
    # ADVICE SLIP API
    adv_data = urllib.request.urlopen("https://api.adviceslip.com/advice")
    adv_readable = adv_data.read()
    adv_d = json.loads(adv_readable)
    slip = adv_d["slip"]
    advice = slip["advice"]

    # PUBLIC HOLIDAY API
    API_KEY0 = open("keys/key_api0.txt", "r").read()
    curr_time = strftime("%m:%d:%y", localtime())
    month = curr_time[:2]
    day = curr_time[3:5]
    year = "20" + curr_time[6:]

    holi_data = urllib.request.urlopen("https://holidays.abstractapi.com/v1/?api_key=" + API_KEY0 + "&country=US&year=" + year + "&month=" + month + "&day=" + day)
    holi_readable = holi_data.read()
    holi_d = json.loads(holi_readable)
    if (len(holi_d) >= 1):
        days = holi_d[0]
        holiday = days["name"]
    else:
        holiday = "No Holiday(s) Today"

    ## WEATHER API
    API_KEY1 = open("keys/key_api1.txt", "r").read()

    weather = urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=New%20York&appid=" + API_KEY1).read()
    weather = json.loads(weather.decode('utf-8'))
    weather_dict = {}
    weather_dict['main'] = weather['weather'][0]['main']
    weather_dict['temp'] = int(9.0/5.0*(weather['main']['temp'] - 273) + 32)


    # DOG PHOTO API
    u = urllib.request.urlopen("https://dog.ceo/api/breeds/image/random")
    response = u.read()
    data = json.loads( response )
    pic = data['message']

    # RETRIEVE USER NOTE
    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()
    c.execute("SELECT content FROM user_note WHERE user_id=?", (str(session.get("user_id")),))
    prev_content = tup_clean(c) # returns list of each element from cursor

    if len(prev_content) > 0: # if the user already had a note saved from a previous session
        note = a_remove(prev_content[0])
    else:
        note = "Write anything here, and click the Save button below to save your work for the future!"

    c.execute("SELECT title, body FROM todo WHERE user_id=? ORDER BY date_time", (str(session.get("user_id")),))
    todo_tuple = list(c)
    num_items_already_in_list = len(todo_tuple)

    if num_items_already_in_list > 0:
        todo_list = convert(todo_tuple)
    else:
        todo_list = []

    return render_template("user_page.html", greeting=get_greeting(session.get("username")), adv=advice, holi=holiday, user_note=note, picture=pic, to_dos=todo_list, weather=weather_dict, route="/")



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
    c.execute("SELECT password, user_id FROM users WHERE username=?", (username,))
    accounts = list(c) #returns tuple
    if len(accounts) != 1 or password != accounts[0][0]:
        return auth_error(is_login_incorrect=True)
    else:
        session['username'] = username # add user and user_id to session for auth purposes
        session['user_id'] = accounts[0][1]
    return root()

@app.route("/create_user", methods=['POST'])
def create_user():
    return render_template('register.html')

'''
register function, registers new users
'''
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()
    c.execute("SELECT username FROM users")

    pre_existing_usernames = convert(list(c))
    print(pre_existing_usernames)

    if [username] in pre_existing_usernames:
        return auth_error(is_user_conflict=True)
    else:
        user_id = uuid4() # generate new uuid for user
        c.execute("INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)", (str(user_id), username, password,))
        session['username'] = str(username)
        session['user_id'] = user_id
        db.commit()
        return user_page()
    return root()


'''
any time user wishes to save notes content, it will come from here
'''
@app.route("/notes_update", methods=["POST"])
def update_note():
    user_id = session.get("user_id")
    new_content = a_clean(request.form["notes"])

    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()

    c.execute("DELETE FROM user_note WHERE user_id=?", (str(user_id),)) # remove old note from db
    c.execute("INSERT INTO user_note (user_id, content) VALUES (?, ?);", (str(user_id), new_content,)) # add new one!
    db.commit()

    return user_page()

@app.route("/clear_all", methods=["POST"])
def clear_todo_list():
    user_id = session.get("user_id")
    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()
    c.execute("DELETE FROM todo WHERE user_id=?", (str(user_id),))
    db.commit()
    return root()

# TODO : bug test and makes sure this works properly
@app.route("/add_item", methods=["POST"])
def add_item_todo():
    user_id = session.get("user_id")
    db = sqlite3.connect(dir + "lame.db") # dir + "blog.db") # connects to sqlite table
    c = db.cursor()

    item_title = request.form['title']
    item_body = request.form['description']
    date_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print(item_title)
    print(item_body)
    print(date_time)

    c.execute("INSERT INTO todo (user_id, title, body, date_time) VALUES (?, ?, ?, ?)", (str(user_id), item_title, item_body, date_time))
    db.commit()
    return root()


@app.route("/delete_item", methods=["POST"])
def delete_item_todo():
    pass


# TODO: remember to delete!
if __name__ == '__main__':
    app.debug = True
    app.run()
