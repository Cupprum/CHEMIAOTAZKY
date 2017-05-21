# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, make_response, session
import random
import json
import uuid
import psycopg2
import os
from urllib.parse import urlparse

app = Flask(__name__)
url = urlparse(os.environ["DATABASE_URL"])
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(db)
conn.autocommit = True
engine = conn.cursor()
engine.execute("CREATE TABLE IF NOT EXISTS FIIT (uuia4 text, meno text, body int, stav text);")

moja = []
uvod = 'Zvol spravne odpovede. Skontroluj svoje odpovede kliknutim na tlacitko kontrola.'


def kont(otazkyzdatabazy):
    A = request.form.get('A')
    if A:
        moja.append('a')
    B = request.form.get('B')
    if B:
        moja.append('b')
    C = request.form.get('C')
    if C:
        moja.append('c')
    D = request.form.get('D')
    if D:
        moja.append('d')
    E = request.form.get('E')
    if E:
        moja.append('e')
    F = request.form.get('F')
    if F:
        moja.append('f')
    G = request.form.get('G')
    if G:
        moja.append('g')
    H = request.form.get('H')
    if H:
        moja.append('h')

    lst = str(otazkyzdatabazy['od']).split(',')

    maxbodovzaodpoved = len(lst)
    mojbodovzaodpoved = 0

    if 'a' in lst and 'a' in moja:
        print('A si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akoma = 'spravne'
    elif 'a' not in moja and 'a' not in lst:
        akoma = 'neutralne'
    else:
        akoma = 'zle'

    if 'b' in lst and 'b' in moja:
        print('B si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomb = 'spravne'
    elif 'b' not in moja and 'b' not in lst:
        akomb = 'neutralne'
    else:
        akomb = 'zle'

    if 'c' in lst and 'c' in moja:
        print('C si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomc = 'spravne'
    elif 'c' not in moja and 'c' not in lst:
        akomc = 'neutralne'
    else:
        akomc = 'zle'

    if 'd' in lst and 'd' in moja:
        print('D si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomd = 'spravne'
    elif 'd' not in moja and 'd' not in lst:
        akomd = 'neutralne'
    else:
        akomd = 'zle'

    if 'e' in lst and 'e' in moja:
        print('E si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akome = 'spravne'
    elif 'e' not in moja and 'e' not in lst:
        akome = 'neutralne'
    else:
        akome = 'zle'

    if 'f' in lst and 'f' in moja:
        print('F si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomf = 'spravne'
    elif 'f' not in moja and 'f' not in lst:
        akomf = 'neutralne'
    else:
        akomf = 'zle'

    if 'g' in lst and 'g' in moja:
        print('G si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomg = 'spravne'
    elif 'g' not in moja and 'g' not in lst:
        akomg = 'neutralne'
    else:
        akomg = 'zle'

    if 'h' in lst and 'h' in moja:
        print('H si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomh = 'spravne'
    elif 'h' not in moja and 'h' not in lst:
        akomh = 'neutralne'
    else:
        akomh = 'zle'

    return maxbodovzaodpoved, mojbodovzaodpoved, akoma, akomb, akomc, akomd, akome, akomf, akomg, akomh


def vyberazdatabazy(otazkyzdatabazy, r):
    otazkyzdatabazy['cislootazky'] = random.choice(r[0:1])
    otazkyzdatabazy['ot'] = random.choice(r[1:2])
    otazkyzdatabazy['od'] = random.choice(r[2:3])
    otazkyzdatabazy['ma'] = random.choice(r[3:4])
    otazkyzdatabazy['mb'] = random.choice(r[4:5])
    otazkyzdatabazy['mc'] = random.choice(r[5:6])
    otazkyzdatabazy['md'] = random.choice(r[6:7])
    otazkyzdatabazy['me'] = random.choice(r[7:8])
    otazkyzdatabazy['mf'] = random.choice(r[8:9])
    otazkyzdatabazy['mg'] = random.choice(r[9:10])
    otazkyzdatabazy['mh'] = random.choice(r[10:11])


def rozborcookie():
    kokie = session['nameID']
    pole = json.loads(kokie)
    randommeno = pole['randommeno']
    mojeotazky = pole['mojeotazky']
    ypsilon = pole['ypsilon']
    body = pole['body']
    koncovka = pole['koncovka']
    zleotazky = pole['zleotazky']
    najmensiaotazka = pole['najmensiaotazka']
    najvacsiaotazka = pole['najvacsiaotazka']
    lastaction = pole['lastaction']
    skupinaotazok = pole['skupinaotazok']
    return randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/', methods=['GET'])
def skusaG():
    kokie = session.get('nameID')
    if kokie is None:
        randommeno = str(uuid.uuid4())
        mojeotazky = []
        ypsilon = 0
        body = 0
        koncovka = 'ok'
        zleotazky = []
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = None
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        print('novy uzivatel', pole)

        jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
        engine.execute(jozo, (randommeno, body))

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    else:
        try:
            kokie = session['nameID']
            pole = json.loads(kokie)
            print('stary uzivatel', pole)
            respond = make_response(render_template('layout.html', uvod=True, bdy=pole['body'], sklonovanie=pole['koncovka']))
            return respond

        except TypeError:
                    randommeno = str(uuid.uuid4())
        mojeotazky = []
        ypsilon = 0
        body = 0
        koncovka = 'ok'
        zleotazky = []
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = None
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        print('novy uzivatel', pole)

        jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
        engine.execute(jozo, (randommeno, body))

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond


@app.route('/', methods=['POST'])
def skusaP():
    if request.form['btn'] == 'Nová otázka':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None
        polesplnenychotazok = set(mojeotazky)
        polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))

        typotazky = "Si skúšaný zo všetkých otázok"
        finalneotazky = list(polevsetkychotazok - polesplnenychotazok)

        if len(finalneotazky) == 0:
            respond = make_response(render_template('layout.html', moznosti=True, control='Nemame otazky', bdy=body, sklonovanie=koncovka))
            return respond

        else:
            ypsilon = random.choice(finalneotazky)

            otazkyzdatabazy = {'cislootazky': None, 'ot': None, 'od': None, 'ma': None, 'mb': None,
                               'mc': None, 'md': None, 'me': None, 'mf': None, 'mg': None, 'mh': None}
            hladavdatabaze = """SELECT * FROM otazky WHERE cislootazky = %s;"""
            engine.execute(hladavdatabaze, (ypsilon,))
            result_set = engine.fetchall()
            for r in result_set:
                vyberazdatabazy(otazkyzdatabazy, r)
                pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                        'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                        'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                print(pole)
                respond = make_response(render_template('layout.html', moznosti=True, checkbuttons=True, typotazok=typotazky, otazka=otazkyzdatabazy['ot'], bdy=body, sklonovanie=koncovka,
                                                        ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'], me=otazkyzdatabazy['me'],
                                                        mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'], control=('Spravna odpoved je', otazkyzdatabazy['od'])))
                session['nameID'] = json.dumps(pole)
                return respond

    if request.form['btn'] == 'Kontrola':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        poslednaaction = lastaction
        lastaction = 'kontrola'

        if str(ypsilon) == '0':
            respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka, control='Ako chceš odpovedať na otázku ktorú nemáš?'))
            return respond

        elif poslednaaction == 'kontrola':
            respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka, control='Kontrola kontroly.'))
            return respond

        else:
            polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))
            polesplnenychotazok = set(mojeotazky)
            finalneotazky = list(polevsetkychotazok - polesplnenychotazok)

            otazkyzdatabazy = {'cislootazky': None, 'ot': None, 'od': None, 'ma': None, 'mb': None,
                               'mc': None, 'md': None, 'me': None, 'mf': None, 'mg': None, 'mh': None}
            hladavdatabaze = """SELECT * FROM otazky WHERE cislootazky = %s;"""

            engine.execute(hladavdatabaze, (ypsilon,))
            result_set = engine.fetchall()
            for r in result_set:
                vyberazdatabazy(otazkyzdatabazy, r)

                maxbodovzaodpoved, mojbodovzaodpoved, akoma, akomb, akomc, akomd, akome, akomf, akomg, akomh = kont(otazkyzdatabazy)

                if maxbodovzaodpoved == mojbodovzaodpoved:
                    moja[:] = []
                    mojeotazky.append(int(ypsilon))
                    body = len(mojeotazky)
                    if body == 1:
                        koncovka = 'ku'
                    elif body == 2 or body == 3 or body == 4:
                        koncovka = 'ky'
                    elif body >= 5:
                        koncovka = 'ok'

                    pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                            'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                            'lastaction': lastaction, 'skupinaotazok': skupinaotazok}

                    jozo = """UPDATE FIIT SET body= %s WHERE uuia4= %s ;"""
                    engine.execute(jozo, (body, randommeno,))

                    respond = make_response(render_template('layout.html', moznosti=True, akoma=akoma, akomb=akomb, akomc=akomc, akomd=akomd,
                                            akome=akome, akomf=akomf, akomg=akomg, akomh=akomh, bdy=body, sklonovanie=koncovka,
                                            control='Výborne, správna odpoveď!', otazka=otazkyzdatabazy['ot'], odp=otazkyzdatabazy['od'],
                                            ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'], me=otazkyzdatabazy['me'],
                                            mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh']))
                    session['nameID'] = json.dumps(pole)
                    return respond

                else:
                    moja[:] = []
                    zleotazky.append(int(ypsilon))
                    pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                            'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                            'lastaction': lastaction, 'skupinaotazok': skupinaotazok}

                    respond = make_response(render_template('layout.html', moznosti=True, akoma=akoma, akomb=akomb, akomc=akomc, akomd=akomd,
                                            akome=akome, akomf=akomf, akomg=akomg, akomh=akomh, bdy=body, sklonovanie=koncovka,
                                            control='Bohužiaľ nesprávne.', otazka=otazkyzdatabazy['ot'], odp=otazkyzdatabazy['od'],
                                            ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'], me=otazkyzdatabazy['me'],
                                            mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh']))
                    session['nameID'] = json.dumps(pole)
                    return respond

    if request.form['btn'] == 'Resetuje otázky':
        starekokie = session['nameID']
        starepole = json.loads(starekokie)
        starerandommeno = starepole['randommeno']

        staryjozo = """DELETE FROM FIIT WHERE uuia4 = %s ;"""
        engine.execute(staryjozo, (starerandommeno, ))

        randommeno = str(uuid.uuid4())
        mojeotazky = []
        ypsilon = 0
        body = 0
        koncovka = 'ok'
        zleotazky = []
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = None

        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}

        jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
        engine.execute(jozo, (randommeno, body))

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Tabuľka najlepších':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None,
                        'tabulka3meno': None, 'tabulka3body': None, 'tabulka4meno': None, 'tabulka4body': None,
                        'tabulka5meno': None, 'tabulka5body': None}
        engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 20;")
        omg = 1
        result_set = engine.fetchall()
        for r in result_set:
            x = random.choice(r[:1])
            y = random.choice(r[1:])
            tabulkovydic['tabulka' + str(omg) + 'meno'] = x
            tabulkovydic['tabulka' + str(omg) + 'body'] = y
            omg += 1

        respond = make_response(render_template('tabulkanajlpesich.html', bdy=body, sklonovanie=koncovka,
                                tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']))
        return respond

    if request.form['btn'] == 'Pridať meno':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        zadanemeno = request.form['vloztemeno']
        lastaction = None

        if zadanemeno == "" or zadanemeno == " ":
            tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None,
                            'tabulka3meno': None, 'tabulka3body': None, 'tabulka4meno': None, 'tabulka4body': None,
                            'tabulka5meno': None, 'tabulka5body': None}
            engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 5;")
            omg = 1
            result_set = engine.fetchall()
            for r in result_set:
                x = random.choice(r[:1])
                y = random.choice(r[1:])
                tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                tabulkovydic['tabulka' + str(omg) + 'body'] = y
                omg += 1
                respond = make_response(render_template('tabulkanajlpesich.html', otazka="Zvoľ iné meno.",
                                        tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                        tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                        tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                        tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                        tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']))
                return respond

        else:
            zistuje = """SELECT * FROM FIIT WHERE meno= %s"""
            engine.execute(zistuje, (zadanemeno,))
            if engine.rowcount == 0:

                jozo = """UPDATE FIIT SET meno= %s WHERE uuia4= %s ;"""
                engine.execute(jozo, (zadanemeno, randommeno))
                fero = """UPDATE FIIT SET stav= '1' WHERE uuia4= %s ;"""
                engine.execute(fero, (randommeno,))

                tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None,
                                'tabulka3meno': None, 'tabulka3body': None, 'tabulka4meno': None, 'tabulka4body': None,
                                'tabulka5meno': None, 'tabulka5body': None}
                engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 5;")
                omg = 1
                result_set = engine.fetchall()
                for r in result_set:
                    x = random.choice(r[:1])
                    y = random.choice(r[1:])
                    tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                    tabulkovydic['tabulka' + str(omg) + 'body'] = y
                    omg += 1

                respond = make_response(render_template('tabulkanajlpesich.html', otazka="Tvoje meno bolo uložené.", bdy=body, sklonovanie=koncovka,
                                        tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                        tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                        tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                        tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                        tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']))
                return respond

            else:
                tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None,
                                'tabulka3meno': None, 'tabulka3body': None, 'tabulka4meno': None, 'tabulka4body': None,
                                'tabulka5meno': None, 'tabulka5body': None}
                engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 5;")
                omg = 1
                result_set = engine.fetchall()
                for r in result_set:
                    x = random.choice(r[:1])
                    y = random.choice(r[1:])
                    tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                    tabulkovydic['tabulka' + str(omg) + 'body'] = y
                    omg += 1

                respond = make_response(render_template('tabulkanajlpesich.html', otazka="Toto meno bolo už použité, skús zadať iné.",
                                        bdy=body, sklonovanie=koncovka,
                                        tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                        tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                        tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                        tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                        tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']))
                return respond

    if request.form['btn'] == 'Zle zodpovedané otázky':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))
        lastaction = None

        if len(zleotazky) == 0:
            respond = make_response(render_template('zleotazky.html', control="Na všetky otázky si odpovedal dobre, nemáš si čo opraviť",
                                    bdy=body, sklonovanie=koncovka))
            return respond

        else:
            ypsilon = random.choice(zleotazky)

            otazkyzdatabazy = {'cislootazky': None, 'ot': None, 'od': None, 'ma': None, 'mb': None,
                               'mc': None, 'md': None, 'me': None, 'mf': None, 'mg': None, 'mh': None}
            hladavdatabaze = """SELECT * FROM otazky WHERE cislootazky = %s;"""
            engine.execute(hladavdatabaze, (ypsilon,))
            result_set = engine.fetchall()
            for r in result_set:
                vyberazdatabazy(otazkyzdatabazy, r)

                pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                        'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                        'lastaction': lastaction, 'skupinaotazok': skupinaotazok}

                respond = make_response(render_template('zleotazky.html', otazka=otazkyzdatabazy['ot'], bdy=body, sklonovanie=koncovka,
                                        ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'], me=otazkyzdatabazy['me'],
                                        mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'], control=('Spravna odpoved je', otazkyzdatabazy['od']),
                                        zleotazky=zleotazky, cislozlejotazky=ypsilon, totosuzleotazky=True))
                session['nameID'] = json.dumps(pole)
                return respond

    if request.form['btn'] == 'Ďalšia zlá otázka':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        if len(zleotazky) == 0:
            respond = make_response(render_template('zleotazky.html', control="Na všetky otázky si odpovedal dobre, nemáš si čo opraviť",
                                                    bdy=body, sklonovanie=koncovka))
            return respond

        else:
            ypsilon = random.choice(zleotazky)

            otazkyzdatabazy = {'cislootazky': None, 'ot': None, 'od': None, 'ma': None, 'mb': None,
                               'mc': None, 'md': None, 'me': None, 'mf': None, 'mg': None, 'mh': None}
            hladavdatabaze = """SELECT * FROM otazky WHERE cislootazky = %s;"""
            engine.execute(hladavdatabaze, (ypsilon,))
            result_set = engine.fetchall()
            for r in result_set:
                vyberazdatabazy(otazkyzdatabazy, r)
                respond = make_response(render_template('zleotazky.html', otazka=otazkyzdatabazy['ot'], bdy=body, sklonovanie=koncovka,
                                        ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'], me=otazkyzdatabazy['me'],
                                        mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'], control=('Spravna odpoved je', otazkyzdatabazy['od']),
                                        zleotazky=zleotazky, cislozlejotazky=ypsilon, totosuzleotazky=True))
                pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                        'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                        'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                session['nameID'] = json.dumps(pole)
                return respond

    if request.form['btn'] == 'Kontrola zlej otázky':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        poslednaaction = lastaction
        lastaction = 'kontrola'

        if poslednaaction == 'kontrola':
            respond = make_response(render_template('zleotazky.html', bdy=body, sklonovanie=koncovka, control='Kontrola kontroly.'))
            return respond
        else:
            if ypsilon in zleotazky:
                otazkyzdatabazy = {'cislootazky': None, 'ot': None, 'od': None, 'ma': None, 'mb': None,
                                   'mc': None, 'md': None, 'me': None, 'mf': None, 'mg': None, 'mh': None}
                hladavdatabaze = """SELECT * FROM otazky WHERE cislootazky = %s;"""
                engine.execute(hladavdatabaze, (ypsilon,))
                result_set = engine.fetchall()
                for r in result_set:
                    vyberazdatabazy(otazkyzdatabazy, r)

                    maxbodovzaodpoved, mojbodovzaodpoved, akoma, akomb, akomc, akomd, akome, akomf, akomg, akomh = kont(otazkyzdatabazy)
                    lst = str(otazkyzdatabazy['od']).split(',')

                    if list(moja) == lst:
                        moja[:] = []
                        zleotazky.remove(int(ypsilon))
                        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                        respond = make_response(render_template('zleotazky.html', control='Vyborne, spravna odpoved!', zleotazky=zleotazky, totosuzleotazky=True))
                        session['nameID'] = json.dumps(pole)
                        return respond

                    else:
                        moja[:] = []
                        respond = make_response(render_template('zleotazky.html', akoma=akoma, akomb=akomb, akomc=akomc, akomd=akomd,
                                                akome=akome, akomf=akomf, akomg=akomg, akomh=akomh,
                                                control='Bohužiaľ nesprávne.', otazka=otazkyzdatabazy['ot'], bdy=body, sklonovanie=koncovka,
                                                ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'], me=otazkyzdatabazy['me'],
                                                mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'],
                                                zleotazky=zleotazky, cislozlejotazky=ypsilon, totosuzleotazky=True))
                        return respond

            else:
                respond = make_response(render_template('zleotazky.html', control='Na všetky otázky si odpovedal správne, nemáš čo opravovať.',
                                        bdy=body, sklonovanie=koncovka))
                return respond

    if request.form['btn'] == 'Zmena skúšaných otázok':
        respond = make_response(render_template('ktoreotazky.html'))
        return respond

    if request.form['btn'] == 'Pridať rozmedzie otázok':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        mensiaotazka = request.form['najmensiaotazka']
        vacsiaotazka = request.form['najvacsiaotazka']

        if len(mensiaotazka) == 0 or len(vacsiaotazka) == 0:
            respond = make_response(render_template('ktoreotazky.html', control='Musíš zadať obe čísla.'))
            return respond

        else:
            najmensiaotazka = int(mensiaotazka)
            najvacsiaotazka = int(vacsiaotazka)

            if najmensiaotazka >= najvacsiaotazka:
                respond = make_response(render_template('ktoreotazky.html', control='Najmenšia otázka musí byť menšia od najväčšej, zároveň si nemôžu byť rovné.'))
                return respond

            if najmensiaotazka <= 0:
                respond = make_response(render_template('ktoreotazky.html', control='Najmenšia otázka musí byť väčšia ako 0.'))
                return respond

            if najvacsiaotazka >= 501:
                respond = make_response(render_template('ktoreotazky.html', control='Najväčšia otázka môže byť maximálne 500.'))
                return respond

            else:
                skupinaotazok = None
                pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                        'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                        'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
                session['nameID'] = json.dumps(pole)
                return respond

    if request.form['btn'] == 'Atóm':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'atom'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Sústava látok':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'sustavalatok'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Látky':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'latky'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Periodická sústava prvkov':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'psustava'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Chemická väzba':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'chvazba'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Názvoslovie':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'nazvoslovie'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Chemické veličiny':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'veliciny'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Kyseliny a zásady':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'kyszas'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Chemické reakcie':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'reakcie'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Chemická rovnováha':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'rovnovaha'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Komplexné zlúčeniny':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'komplexy'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'Príklady':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None

        skupinaotazok = 'priklady'
        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        session['nameID'] = json.dumps(pole)
        return respond

    if request.form['btn'] == 'O projekte':
        respond = make_response(render_template('oProjekte.html'))
        return respond

    if request.form['btn'] == 'Prejsť na otázku':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))
        polesplnenychotazok = set(mojeotazky)
        lastaction = None

        try:
            if int(request.form['cislootazky']) in list(range(1, 500 + 1)):
                ypsilon = int(request.form['cislootazky'])

                otazkyzdatabazy = {'cislootazky': None, 'ot': None, 'od': None, 'ma': None, 'mb': None,
                                   'mc': None, 'md': None, 'me': None, 'mf': None, 'mg': None, 'mh': None}
                hladavdatabaze = """SELECT * FROM otazky WHERE cislootazky = %s;"""
                engine.execute(hladavdatabaze, (ypsilon,))
                result_set = engine.fetchall()
                for r in result_set:
                    vyberazdatabazy(otazkyzdatabazy, r)
                    pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                            'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                            'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                    respond = make_response(render_template('jednaotazka.html', otazka=otazkyzdatabazy['ot'],
                                            ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'],
                                            me=otazkyzdatabazy['me'], mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'],
                                            control=('Spravna odpoved je', otazkyzdatabazy['od']), bdy=body, sklonovanie=koncovka))
                    session['nameID'] = json.dumps(pole)
                    return respond
            else:
                respond = make_response(render_template('jednaotazka.html', control='something went wrong', bdy=body, sklonovanie=koncovka))
                return respond

        except ValueError:
            respond = make_response(render_template('jednaotazka.html', otazka="""moj mily :) je pekne ze si myslis ze ta to
                                    bude skusat pismenka :D ale takto to nefunguje :D alebo si zadal cislo vacsie ako 500, koniec koncou
                                    si retard a ak sa ti nepaci ze ti tu teraz pindam tak v pravo hore mas tlacitko co vyriesi vsetky tvoje problemy""",
                                    bdy=body, sklonovanie=koncovka))
            return respond

    if request.form['btn'] == 'Kontrola otázky':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        poslednaaction = lastaction
        lastaction = 'kontrola'
        polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))
        polesplnenychotazok = set(mojeotazky)
        finalneotazky = list(polevsetkychotazok - polesplnenychotazok)

        if poslednaaction == 'kontrola':
            respond = make_response(render_template('jednaotazka.html', bdy=body, sklonovanie=koncovka, control='Na otázku už nemôžeš odpovedať.'))
            return respond

        elif ypsilon == 0:
            respond = make_response(render_template('jednaotazka.html', bdy=body, sklonovanie=koncovka, control='A co by si rád kontroloval, keď nemás zadanú otázku.'))
            return respond

        else:
            otazkyzdatabazy = {'cislootazky': None, 'ot': None, 'od': None, 'ma': None, 'mb': None,
                               'mc': None, 'md': None, 'me': None, 'mf': None, 'mg': None, 'mh': None}
            hladavdatabaze = """SELECT * FROM otazky WHERE cislootazky = %s;"""
            engine.execute(hladavdatabaze, (ypsilon,))
            result_set = engine.fetchall()
            for r in result_set:
                vyberazdatabazy(otazkyzdatabazy, r)
                maxbodovzaodpoved, mojbodovzaodpoved, akoma, akomb, akomc, akomd, akome, akomf, akomg, akomh = kont(otazkyzdatabazy)
                lst = str(otazkyzdatabazy['od']).split(',')

                if list(moja) == lst:
                    moja[:] = []
                    if int(ypsilon) not in mojeotazky:
                        mojeotazky.append(int(ypsilon))
                    body = len(mojeotazky)
                    if body == 1:
                        koncovka = 'ku'
                    elif body == 2 or body == 3 or body == 4:
                        koncovka = 'ky'
                    elif body >= 5:
                        koncovka = 'ok'
                    pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                            'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                            'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                    jozo = """UPDATE FIIT SET body= %s WHERE uuia4= %s ;"""
                    engine.execute(jozo, (body, randommeno,))

                    respond = make_response(render_template('jednaotazka.html', akoma=akoma, akomb=akomb, akomc=akomc, akomd=akomd,
                                            akome=akome, akomf=akomf, akomg=akomg, akomh=akomh, bdy=body, sklonovanie=koncovka,
                                            control='Vyborne, spravna odpoved!', otazka=otazkyzdatabazy['ot'],
                                            ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'],
                                            me=otazkyzdatabazy['me'], mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh']))
                    session['nameID'] = json.dumps(pole)
                    return respond


app.secret_key = os.environ["SESSION_KEY"]


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
