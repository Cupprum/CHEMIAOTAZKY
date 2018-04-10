from flask import (
    Flask, request, render_template, make_response, session, url_for, redirect)
import random
import json
import uuid
import os


app = Flask(__name__)

@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        return respond
