from flask import (
    Flask, request, render_template, make_response, session, url_for, redirect)
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import os
import operator


app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.environ["SESSION_KEY"]

mongodb_uri = os.environ["MONGODB_URI"]
client = MongoClient(mongodb_uri)

if mongodb_uri == "mongodb://localhost:27017/":
    db = client.chemia

else:
    db = client.heroku_847wntjv

qtable = db.table_questions
utable = db.table_users
ltable = db.table_lists


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
            "correct_answers": [],
            "wrong_answers": [],
            "points": 0,
            "lat_q_num": None,
            "lat_q_ans": None,
            "group": "",
            "small": 0,
            "high": 1500,
            "desired": None}

    utable.find_one_and_replace(old_user, user)


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        user_id = session.get('nameID')
        user = utable.find_one({"_id": ObjectId(user_id)})

        if user is None:
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

        elif request.form['btn'] == 'Zle zodpovedané otázky':
            respond = make_response(redirect(url_for('wrong_answered')))
            return respond


@app.route('/otazka', methods=['GET', 'POST'])
def questions():
    if request.method == 'GET':
        user_id = session.get('nameID')
        user_par = {"_id": ObjectId(user_id)}
        user = utable.find_one(user_par)

        if user['group'] != "":
            help_var = ltable.find_one({"name_of_list": user['group']})
            list_q_from_cat = help_var['lst']

            counter = 0
            for x in range(len(list_q_from_cat)):
                if list_q_from_cat[x] not in user["correct_answers"]:
                    break
                else:
                    counter += 1

                if counter == len(list_q_from_cat):
                    utable.find_one_and_update(
                        user_par, {"$set": {"group": ""}})
                    respond = make_response(redirect(url_for('questions')))
                    return respond

            while True:
                num_of_q = random.choice(list_q_from_cat)
                if num_of_q not in user["correct_answers"]:
                    break

        else:
            while True:
                num_of_q = random.randint(user["small"], user["high"])
                if num_of_q not in user["correct_answers"]:
                    break

        if user['desired'] is not None:
            num_of_q = user['desired']

            utable.find_one_and_update(
                user_par, {"$set": {"desired": None}})

        print(num_of_q)
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
                                                typotazok=user['group'],
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

            elif user['lat_q_num'] not in user['wrong_answers']:
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

        elif request.form['btn'] == 'Zle zodpovedané otázky':
            respond = make_response(redirect(url_for('wrong_answered')))
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

            respond = make_response(redirect(url_for('table')))
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
        help_var = ltable.find_one({"name_of_list": 'list_of_categories'})
        list_of_categories = help_var['lst']

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

        elif request.form['btn'] in list_of_categories:
            for x in list_of_categories:
                if request.form['btn'] == x:
                    user_id = session.get('nameID')
                    user_par = {"_id": ObjectId(user_id)}

                    utable.find_one_and_update(
                        user_par, {"$set": {"group": x}})

                    respond = make_response(redirect(url_for('questions')))
                    return respond

        elif request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond


@app.route('/wrong_answered', methods=['GET', 'POST'])
def wrong_answered():
    if request.method == 'GET':
        user_id = session.get('nameID')
        user_par = {"_id": ObjectId(user_id)}
        user = utable.find_one(user_par)
        wrong_answers = user['wrong_answers']

        dic_wrong = {}
        for x in range(0, len(wrong_answers) + 5, 5):
            list_help = []
            for y in range(5):
                try:
                    list_help.append(wrong_answers[x + y])
                except IndexError:
                    dic_wrong.update({str(int(x / 5)): list_help})
                    break
            dic_wrong.update({str(int(x / 5)): list_help})

        will_delete = []
        for x in dic_wrong:
            if len(dic_wrong[x]) == 0:
                will_delete.append(x)

        for x in will_delete:
            dic_wrong.pop(x)

        print(dic_wrong)

        respond = make_response(render_template('zleotazky.html',
                                                dic=dic_wrong))
        return respond

    elif request.method == 'POST':
        user_id = session.get('nameID')
        user_par = {"_id": ObjectId(user_id)}
        user = utable.find_one(user_par)

        if request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond

        else:
            utable.find_one_and_update(
                user_par, {"$set": {"desired": int(request.form['btn'])}})

            respond = make_response(redirect(url_for('questions')))
            return respond


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        respond = make_response(render_template('login.html'))
        return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'Potvrdit heslo':
            possible_password = request.form['password']

            if possible_password == app.secret_key:
                respond = make_response(redirect(url_for('home')))
                return respond

            else:
                str_yell = 'YOU SHALL NOT PASS'

                respond = make_response(render_template('login.html',
                                                        yell=str_yell))
                return respond


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)
