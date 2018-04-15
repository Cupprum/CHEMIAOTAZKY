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
                    "small": 0,
                    "high": 1500,
                    "correct_answers": [],
                    "wrong_answers": [],
                    "points": 0,
                    "lat_q_num": None,
                    "lat_q_ans": None}

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
            respond = make_response(redirect(url_for('questions')))
            return respond


@app.route('/otazka', methods=['GET', 'POST'])
def questions():
    if request.method == 'GET':
        user_id = session.get('nameID')
        user_par = {"_id": ObjectId(user_id)}
        user = utable.find_one(user_par)

        while True:
            num_of_q = random.randint(user["small"], user["high"])
            if num_of_q not in user["correct_answers"]:
                break

        question = qtable.find_one({"possition": num_of_q})
        utable.find_one_and_update(user_par, {"$set": {"lat_q_num": num_of_q}})

        my_points = user["points"]
        ending = what_ending(my_points)

        list1 = ["a", "b", "c", "d",
                 "e", "f", "g", "h"]

        list2 = ["A", "B", "C", "D",
                 "E", "F", "G", "H"]

        list3 = list1[:]

        list4 = [question['ma'],
                 question['mb'],
                 question['mc'],
                 question['md'],
                 question['me'],
                 question['mf'],
                 question['mg'],
                 question['mh']]

        respond = make_response(render_template('otazka.html',
                                                moznosti=True,
                                                otazka=question['ot'],
                                                my_points=user['points'],
                                                sklonovanie=ending,
                                                odp=question['od'],
                                                list1=list1,
                                                list2=list2,
                                                list3=list3,
                                                list4=list4))
        return respond

    elif request.method == 'POST':
        user_id = session.get('nameID')
        user = utable.find_one({"_id": ObjectId(user_id)})
        pprint.pprint(user)
        if request.form['btn'] == 'Kontrola':
            return 'Kontrola'


        elif request.form['btn'] == 'Nová otázka':
            respond = make_response(redirect(url_for('questions')))
            return respond


app.secret_key = os.environ["SESSION_KEY"]


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
