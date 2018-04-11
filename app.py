from flask import (
    Flask, request, render_template, make_response, session, url_for, redirect)
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import os
import pprint


app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.chemia
qtable = db.table_questions
utable = db.table_users


def what_ending(my_points):
    if my_points == 0 or my_points >= 5:
        ending = "ok"
    elif my_points == 1:
        ending = "ku"
    elif my_points > 0 and my_points < 5:
        ending = "ky"
    return ending


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        user_id = session.get('nameID')
        if user_id is None:
            user = {"my_chosen_name": "",
                    "group": "",
                    "smallest": 0,
                    "highest": 1500,
                    "correct_answers": [],
                    "wrong_answers": [],
                    "points": 0}

            new_user_id = utable.insert_one(user).inserted_id
            session['nameID'] = str(new_user_id)

        else:
            user = utable.find_one({"_id": ObjectId(user_id)})

        my_points = user["points"]

        ending = what_ending(my_points)

        respond = make_response(render_template('layout.html',
                                                uvod=True,
                                                my_points=my_points,
                                                sklonovanie=ending))
        return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'Nová otázka':
            respond = make_response(redirect(url_for('question')))


@app.route('/otazka', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':

app.secret_key = os.environ["SESSION_KEY"]


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
