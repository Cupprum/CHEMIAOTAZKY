from flask import (
    Flask, request, render_template, make_response,
    session, url_for, redirect, jsonify)
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from pymongo import MongoClient
import random
import os
import time
import operator
import uuid
from uuid import getnode as get_mac
import paypalrestsdk


app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='chemiaotazky@gmail.com',
    MAIL_PASSWORD='MP14759631478965')
mail = Mail(app)

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "ATEq1XVImz9J9X93C0RQzADQT17lqxO0K7FUZbq1pCC2LjkUUcrgvZtgK7jmKQj_-WsxyBczuQQ9IduV",
    "client_secret": "ECAIqVBgaKf2s08bU6JUjL8DDC-6LgWKVLfPp4oirtS7haBTmGYzPBvD9u3gDVQSCc8oNmtbjT2ZNXLv"})

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
    user_id = session.get('loged')
    old_user = utable.find_one({"my_name": user_id})

    user = {"my_name": old_user['my_name'],
            "my_mail": old_user['my_mail'],
            "my_password": old_user['my_password'],
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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        user_id = session.get('loged')
        user_par = {"my_name": user_id}

        if user_id is not None:
            user = utable.find_one(user_par)
            try:
                if len(user) != 14:
                    session['loged'] = None

                    utable.remove(user_par)

                    respond = make_response(redirect(url_for('register')))
                    return respond
            except TypeError:
                respond = make_response(redirect(url_for('register')))
                return respond

        else:
            respond = make_response(redirect(url_for('login')))
            return respond

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
        user_id = session.get('loged')
        user_par = {"my_name": user_id}
        user = utable.find_one(user_par)

        if user_id is not None:
            user = utable.find_one({"my_name": user_id})

        else:
            respond = make_response(redirect(url_for('login')))
            return respond

        if user is None:
            session['loged'] = None
            respond = make_response(redirect(url_for('login')))
            return respond

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
            list_possible = list(range(user["small"], user["high"] + 1))
            list_correct = user["correct_answers"]
            if set(list_possible).issubset(list_correct):
                utable.find_one_and_update(
                    user_par, {"$set": {"small": 0}})
                utable.find_one_and_update(
                    user_par, {"$set": {"high": 1500}})

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

        str_odp = ""

        try:
            if session['admin'] is True:
                str_odp = question['od']

        except KeyError:
            session['admin'] = False

        actual_mac = hex(get_mac())
        actual_time = time.time()

        # mozno to nebude treba az tak komplikovane, zistim ked to skusim online
        if actual_mac in user['mac']:
            utable.find_one_and_update(user_par, {"$set": {
                f'mac.{actual_mac}': actual_time}})

        else:
            utable.find_one_and_update(user_par, {"$set": {
                f'mac.{actual_mac}': actual_time}})

        respond = make_response(render_template('otazka.html',
                                                moznosti=True,
                                                control_button=True,
                                                typotazok=user['group'],
                                                otazka=question['ot'],
                                                my_points=my_points,
                                                sklonovanie=ending,
                                                odp=str_odp,
                                                list1=list1,
                                                list2=list2,
                                                list3=list3,
                                                list4=list4))
        return respond

    elif request.method == 'POST':
        user_id = session.get('loged')
        user_par = {"my_name": user_id}
        user = utable.find_one(user_par)

        if user is None or user_id is None:
            session['loged'] = None
            respond = make_response(redirect(url_for('login')))
            return respond

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

            str_odp = ""

            if session['admin'] is True:
                str_odp = question['od']

            respond = make_response(render_template('otazka.html',
                                                    moznosti=True,
                                                    otazka=question['ot'],
                                                    my_points=my_points,
                                                    sklonovanie=ending,
                                                    odp=str_odp,
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
        all_people = utable.find({"my_name": {"$ne": ""}})

        dic_people = {}
        for x in all_people:
            dic_people.update({x['my_name']: x['points']})

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
        if request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond


@app.route('/changequestions', methods=['GET', 'POST'])
def changequestions():
    if request.method == 'GET':
        user_id = session.get('loged')

        if user_id is not None:
            respond = make_response(render_template('zmenaotazok.html'))
            return respond

        else:
            respond = make_response(redirect(url_for('login')))
            return respond

    elif request.method == 'POST':
        help_var = ltable.find_one({"name_of_list": 'list_of_categories'})
        list_of_categories = help_var['lst']

        if request.form['btn'] == 'Resetovanie vyberania otazok':
            user_id = session.get('loged')
            user_par = {"my_name": user_id}

            user = utable.find_one(user_par)
            print(f"1 {user}")

            help_list1 = ["group", "small", "high"]
            help_list2 = ["", 0, 1500]

            for x in range(2):
                utable.find_one_and_update(user_par, {"$set": {
                    help_list1[x]: help_list2[x]}})

            user = utable.find_one(user_par)
            print(f"2 {user}")

            respond = make_response(redirect(url_for('home')))
            return respond

        elif request.form['btn'] == 'Pridať rozmedzie otázok':
            user_id = session.get('loged')
            user_par = {"my_name": user_id}

            smallest = int(request.form['najmensiaotazka'])
            highest = int(request.form['najvacsiaotazka'])

            utable.find_one_and_update(
                user_par, {"$set": {"small": smallest}})

            utable.find_one_and_update(
                user_par, {"$set": {"high": highest}})

            utable.find_one_and_update(
                user_par, {"$set": {"group": ""}})

            respond = make_response(redirect(url_for('home')))
            return respond

        elif request.form['btn'] == 'Prejsť na otázku':
            user_id = session.get('loged')
            user_par = {"my_name": user_id}

            dreamed_question = int(request.form['cislootazky'])

            utable.find_one_and_update(
                user_par, {"$set": {"desired": dreamed_question}})

            respond = make_response(redirect(url_for('questions')))
            return respond

        elif request.form['btn'] in list_of_categories:
            for x in list_of_categories:
                if request.form['btn'] == x:
                    user_id = session.get('loged')
                    user_par = {"my_name": user_id}

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
        user_id = session.get('loged')
        user_par = {"my_name": user_id}
        user = utable.find_one(user_par)

        if user_id is not None:
            user = utable.find_one({"my_name": user_id})

        else:
            respond = make_response(redirect(url_for('login')))
            return respond

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

        respond = make_response(render_template('zleotazky.html',
                                                dic=dic_wrong))
        return respond

    elif request.method == 'POST':
        user_id = session.get('loged')
        user_par = {"my_name": user_id}

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
        user_id = session.get('loged')

        if user_id is not None:
            respond = make_response(redirect(url_for('home')))
            return respond

        respond = make_response(render_template('login.html'))
        return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'login':
            possible_name = request.form['name']
            possible_pass = request.form['password']

            if possible_pass == app.secret_key and possible_name == 'admin':
                session['admin'] = True
                session['loged'] = request.form['name']

                respond = make_response(redirect(url_for('home')))
                return respond

            else:
                session['admin'] = False

                user_par = {"my_name": request.form['name']}
                user = utable.find_one(user_par)

                try:
                    if user['my_password'] == request.form['password']:
                        session['loged'] = request.form['name']
                        respond = make_response(redirect(url_for('home')))
                        return respond

                except TypeError:
                    yell_msg = 'Zle zadane prihlasovacie udaje'
                    respond = make_response(render_template('login.html',
                                                            yell=yell_msg))
                    return respond

        elif request.form['btn'] == 'Registracia':
            respond = make_response(redirect(url_for('register')))
            return respond

        elif request.form['btn'] == 'Zabudnute heslo':
            respond = make_response(redirect(url_for('forgotten_password')))
            return respond

        elif request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        user_id = session.get('loged')

        if user_id is not None:
            respond = make_response(redirect(url_for('home')))
            return respond

        respond = make_response(render_template('register.html'))
        return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'Zaregistrovat':
            potential_name = request.form['name']
            potential_mail = request.form['mail']
            potential_password = request.form['password1']
            potential_password_check = request.form['password2']

            if potential_password != potential_password_check:
                yell_msg = 'Hesla sa nezhoduju'
                respond = make_response(render_template('register.html',
                                                        yell=yell_msg))
                return respond

            if len(potential_name) > 0 \
               and len(potential_mail) > 0 \
               and len(potential_password) > 0:

                name_check = utable.find_one({"my_name": potential_name})
                mail_check = utable.find_one({"my_mail": potential_mail})

                if name_check is None and mail_check is None:

                    actual_mac = hex(get_mac())
                    actual_time = time.time()

                    mac_adresses = {actual_mac: actual_time}

                    user = {"my_name": potential_name,
                            "my_mail": potential_mail,
                            "my_password": potential_password,
                            "correct_answers": [],
                            "wrong_answers": [],
                            "points": 0,
                            "lat_q_num": None,
                            "lat_q_ans": None,
                            "group": "",
                            "small": 0,
                            "high": 1500,
                            "desired": None,
                            "mac": mac_adresses}

                    activation_code = str(uuid.uuid4())

                    text_msg = f'<p> meno {potential_name}</p>\
                                 <p> heslo {potential_password}</p>\
                                 <p> aktivacny kod {activation_code}</p>'
                    try:
                        msg = Message("Tvoje prihlasovacie udaje",
                                      sender="chemiaotazky@gmail.com",
                                      recipients=[potential_mail])
                        msg.html = text_msg
                        mail.send(msg)

                    except Exception as e:
                        yell_msg = 'Neplatny mail'
                        respond = make_response(
                            render_template('register.html',
                                            yell=yell_msg))
                        return respond

                    utable.insert_one(user)
                    session['admin'] = False
                    session['activate'] = [activation_code, potential_name]

                    respond = make_response(redirect(url_for('activate')))
                    return respond

                elif name_check is not None:
                    yell_msg = 'Toto meno nemozes pouzit'
                    respond = make_response(render_template('register.html',
                                                            yell=yell_msg))
                    return respond

                elif mail_check is not None:
                    yell_msg = 'Tento mail je uz pouzity'
                    respond = make_response(render_template('register.html',
                                                            yell=yell_msg))
                    return respond

            yell_msg = 'Musis zadat vsetky udaje'
            respond = make_response(render_template('register.html',
                                                    yell=yell_msg))
            return respond

        elif request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond


@app.route('/activate', methods=['GET', 'POST'])
def activate():
    if request.method == 'GET':
        activation_code = session.get('activate')[0]
        potential_name = session.get('activate')[1]

        if activation_code is not None:
            yell_msg = 'Zadajte aktivacny kod ktory vam bol zaslany na mail'
            respond = make_response(render_template('activate.html',
                                                    yell=yell_msg))
            return respond

        else:
            respond = make_response(redirect(url_for('home')))
            return respond

    if request.method == 'POST':
        if request.form['btn'] == 'approve':
            activation_code_my = request.form['activation_code']

            activation_code_real = session.get('activate')[0]
            potential_name = session.get('activate')[1]

            if activation_code_my == activation_code_real:
                session['loged'] = potential_name
                session['activate'] = None

                respond = make_response(redirect(url_for('home')))
                return respond

            else:
                yell_msg = 'Neplatny kod'
                respond = make_response(render_template('activate.html',
                                                        yell=yell_msg))
                return respond

        elif request.form['btn'] == 'Tabuľka najlepších':
            respond = make_response(redirect(url_for('table')))
            return respond

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            respond = make_response(redirect(url_for('changequestions')))
            return respond


@app.route('/forgotten_password', methods=['GET', 'POST'])
def forgotten_password():
    if request.method == 'GET':
        already_done = session.get('forgotten')
        print(already_done)

        yell_msg = 'Zadaj svoj email'
        respond = make_response(render_template('forgotten.html',
                                                yell=yell_msg))
        return respond

    if request.method == 'POST':
        if request.form['btn'] == 'approve':
            entered_mail = request.form['mail']

            try:
                user_par = {"my_mail": entered_mail}
                user = utable.find_one(user_par)

                text_msg = f'<p> meno {user["my_name"]}</p>\
                             <p> heslo {user["my_password"]}</p>'

                msg = Message("Tvoje prihlasovacie udaje",
                              sender="chemiaotazky@gmail.com",
                              recipients=[entered_mail])

                msg.html = text_msg
                mail.send(msg)

            except Exception as e:
                yell_msg = 'Neplatny mail'
                respond = make_response(
                    render_template('forgotten.html',
                                    yell=yell_msg))
                return respond

            yell_msg = 'Prihlasovacie udaje boli poslane na zadany mail'
            respond = make_response(render_template('forgotten.html',
                                                    yell=yell_msg))
            return respond


@app.route('/subscription', methods=['GET', 'POST'])
def subscription():
    if request.method == 'GET':
        respond = make_response(render_template('subscription.html'))
        return respond


@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Poplatok za registraciu",
                    "sku": "item",
                    "price": "5.00",
                    "currency": "EUR",
                    "quantity": 1}]},
            "amount": {
                "total": "5.00",
                "currency": "EUR"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('successful')
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})


@app.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('executed')
        success = True
    else:
        print(payment.error)

    return jsonify({'success': success})


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, use_reloader=True)
