from flask import (
    Flask, request, render_template, make_response, session, url_for, redirect)
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import os
import pprint
import operator


app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.chemia
qtable = db.table_questions
utable = db.table_users


class table_obj:
    def __init__(self, name, points):
        self.name = name
        self.points = points


def what_ending(my_points):
    if my_points == 0 or my_points >= 5:
        ending = "ok"
    elif my_points == 1:
        ending = "ku"
    elif my_points > 0 and my_points < 5:
        ending = "ky"
    return ending


def reset():
    user_id = session.get('nameID')
    user_par = {"_id": ObjectId(user_id)}
    old_user = utable.find_one(user_par)

    user = {"my_chosen_name": "",
            "group": "",
            "small": 0,
            "high": 1500,
            "correct_answers": [],
            "wrong_answers": [],
            "points": 0,
            "lat_q_num": None,
            "lat_q_ans": None}

    utable.find_one_and_replace(old_user, user)


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        user_id = session.get('nameID')
        if user_id is None:
            user = {"my_chosen_name": "",
                    "correct_answers": [],
                    "wrong_answers": [],
                    "points": 0,
                    "lat_q_num": None,
                    "lat_q_ans": None,
                    "group": "",
                    "small": 0,
                    "high": 1500,
                    "desired": None}

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

        elif request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond

        elif request.form['btn'] == 'Resetuje otázky':
            reset()
            respond = make_response(redirect(url_for('home')))
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

        if user['desired'] is not None:
            num_of_q = user['desired']

            utable.find_one_and_update(
                user_par, {"$set": {"desired": None}})

        question = qtable.find_one({"possition": num_of_q})
        utable.find_one_and_update(
            user_par, {"$set": {"lat_q_num": num_of_q}})
        utable.find_one_and_update(
            user_par, {"$set": {"lat_q_ans": question["od"]}})

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
                                                control_button=True,
                                                otazka=question['ot'],
                                                my_points=my_points,
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

        if request.form['btn'] == 'Kontrola':
            question = qtable.find_one({"possition": user['lat_q_num']})

            list1 = ["a", "b", "c", "d",
                     "e", "f", "g", "h"]

            list2 = ["A", "B", "C", "D",
                     "E", "F", "G", "H"]

            list4 = [question['ma'],
                     question['mb'],
                     question['mc'],
                     question['md'],
                     question['me'],
                     question['mf'],
                     question['mg'],
                     question['mh']]

            list_correct = str(user["lat_q_ans"]).split(",")

            list_my = []
            for x in range(8):
                zadane = request.form.get(list2[x])
                if zadane is not None:
                    list_my.append(zadane.lower())

            list3 = []

            for x in list1:
                if x in list_correct and x in list_my:
                    list3.append(1)
                elif x not in list_correct and x not in list_my:
                    list3.append(1)
                else:
                    list3.append(0)

            list1 = []
            for x in range(8):
                zadane = request.form.get(list2[x])
                if zadane is None:
                    list1.append(0)
                else:
                    list1.append(1)

            user_par = {"_id": ObjectId(user_id)}

            if list3.count(1) == 8:
                utable.find_one_and_update(user_par, {"$inc": {"points": 1}})
                utable.find_one_and_update(user_par, {"$push": {
                    "correct_answers": user['lat_q_num']}})

                if user['lat_q_num'] in user["wrong_answers"]:
                    utable.find_one_and_update(user_par, {"$pull": {
                        "wrong_answers": user['lat_q_num']}})

            else:
                utable.find_one_and_update(user_par, {"$push": {
                    "wrong_answers": user['lat_q_num']}})

            user = utable.find_one(user_par)
            my_points = user["points"]
            ending = what_ending(my_points)

            respond = make_response(render_template('otazka.html',
                                                    moznosti=True,
                                                    otazka=question['ot'],
                                                    my_points=my_points,
                                                    sklonovanie=ending,
                                                    odp=question['od'],
                                                    list1=list1,
                                                    list2=list2,
                                                    list3=list3,
                                                    list4=list4))

            return respond

        elif request.form['btn'] == 'Nová otázka':
            respond = make_response(redirect(url_for('questions')))
            return respond

        elif request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond

        elif request.form['btn'] == 'Resetuje otázky':
            reset()
            respond = make_response(redirect(url_for('home')))
            return respond


@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'GET':
        all_people = utable.find({"my_chosen_name": {"$ne": ""}})

        dic_people = {}
        for x in all_people:
            dic_people.update({x['my_chosen_name']: x['points']})

        sorted_people = sorted(dic_people.items(),
                               key=operator.itemgetter(1),
                               reverse=True)

        list_of_names = []
        list_of_points = []
        list_of_numbers = ["1.", "2.", "3.", "4.", "5."]

        for x in sorted_people:
            list_of_names.append(x[0])
            list_of_points.append(x[1])

        respond = make_response(render_template('tabulkanajlepsich.html',
                                                list1=list_of_numbers,
                                                list2=list_of_names,
                                                list3=list_of_points))
        return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'Pridať meno':
            user_id = session.get('nameID')
            user_par = {"_id": ObjectId(user_id)}

            name = request.form['vloztemeno']
            utable.find_one_and_update(user_par, {"$set": {
                "my_chosen_name": name}})

            respond = make_response(redirect(url_for('home')))
            return respond

        elif request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond


@app.route('/changequestions', methods=['GET', 'POST'])
def changequestions():
    if request.method == 'GET':
        respond = make_response(render_template('zmenaotazok.html'))
        return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'Pridať rozmedzie otázok':
            user_id = session.get('nameID')
            user_par = {"_id": ObjectId(user_id)}

            smallest = int(request.form['najmensiaotazka'])
            highest = int(request.form['najvacsiaotazka'])

            utable.find_one_and_update(
                user_par, {"$set": {"small": smallest}})

            utable.find_one_and_update(
                user_par, {"$set": {"high": highest}})

            respond = make_response(redirect(url_for('home')))
            return respond

        elif request.form['btn'] == 'Prejsť na otázku':
            user_id = session.get('nameID')
            user_par = {"_id": ObjectId(user_id)}

            dreamed_question = int(request.form['cislootazky'])

            utable.find_one_and_update(
                user_par, {"$set": {"desired": dreamed_question}})

            respond = make_response(redirect(url_for('questions')))
            return respond

        elif request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond


app.secret_key = os.environ["SESSION_KEY"]


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
