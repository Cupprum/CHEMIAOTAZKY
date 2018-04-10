from flask import (
    Flask, request, render_template, make_response, session, url_for, redirect)
import random
import uuid
import os
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.chemia
qtable = db.table_questions
utable = db.table_users


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        user_name = session.get('nameID')
        if user_name is None:
            new_user_name = str(uuid.uuid4())
            dic_user = {"name": new_user_name,
                        "correct_answers": [],
                        "wrong_answers": [],
                        "points": 0}

            session['nameID'] = new_user_name
            utable.insert_one(dic_user)

        else:
            print(f"greetings summoner {user_name}")

        respond = make_response(render_template('layout.html',
                                                uvod=True))
        return respond


app.secret_key = os.environ["SESSION_KEY"]


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
