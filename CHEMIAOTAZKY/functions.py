from CHEMIAOTAZKY.__init__ import utable
from flask import session


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
