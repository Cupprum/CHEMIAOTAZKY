from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from pymongo import MongoClient
import os
import paypalrestsdk

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='chemiaotazky@gmail.com',
    MAIL_PASSWORD='MP14759631478965')
mail = Mail(app)

Bootstrap(app)
app.secret_key = os.environ["SESSION_KEY"]

mongodb_uri = os.environ["MONGODB_URI"]
client = MongoClient(mongodb_uri)

if mongodb_uri == "mongodb://localhost:27017/":
    db = client.chemia
    environment = 'sandbox'

else:
    db = client.heroku_847wntjv
    environment = 'live'

paypalrestsdk.configure({
    "mode": environment,
    "client_id": os.environ["PAYPAL_ID"],
    "client_secret": os.environ["PAYPAL_SECRET"]})

qtable = db.table_questions
utable = db.table_users
ltable = db.table_lists

from CHEMIAOTAZKY.views import *
