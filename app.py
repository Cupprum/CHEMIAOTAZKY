from flask import Flask, request, render_template, make_response
import flask.views
import random
import xml.etree.ElementTree as ET
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
engine.execute("CREATE TABLE IF NOT EXISTS FIIT (uuia4 text, meno text, body text, stav text);")


jozo = """INSERT INTO fiit (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
engine.execute(jozo, ('hatlanina', 2))
tree = ET.parse('chemia.xml')
root = tree.getroot()
moja = []
ID = []
otazka = []
uvod = 'Zvol spravne odpovede. Skontroluj svoje odpovede kliknutim na tlacitko kontrola.'


def kont():
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


@app.route('/', methods=['GET'])
def get():
    if request.cookies.get('nameID') is None:
        randommeno = str(uuid.uuid4())
        mojeotazky = []
        ypsilon = 0
        body = 0
        koncovka = 'ok'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka)
        print('toto vypise kookie noveho uzivatela', pole)

        jozo = """INSERT INTO fiit (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
        engine.execute(jozo, (randommeno, body))

        tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
        engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 10;")
        omg = 1
        result_set = engine.fetchall()
        for r in result_set:
            x = random.choice(r[:1])
            y = random.choice(r[1:])
            tabulkovydic['tabulka' + str(omg) + 'meno'] = x
            tabulkovydic['tabulka' + str(omg) + 'body'] = y
            omg += 1

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka,
                                tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body']))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    else:
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        print('stary uzivatel', pole)
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]

        tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
        engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 10;")
        omg = 1
        result_set = engine.fetchall()
        for r in result_set:
            x = random.choice(r[:1])
            y = random.choice(r[1:])
            tabulkovydic['tabulka' + str(omg) + 'meno'] = x
            tabulkovydic['tabulka' + str(omg) + 'body'] = y
            omg += 1

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovaie=koncovka,
                                                tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                                tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body']))
        return respond


@app.route('/', methods=['POST'])
def post():
    if request.form['btn'] == 'Nova otazka':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        polevsetkychotazok = set(list(range(1, 500 + 1)))
        mojeotazky = random.choice(list(pole[1:2]))
        polesplnenychotazok = set(mojeotazky)
        finalneotazky = list(polevsetkychotazok - polesplnenychotazok)
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        print("mojeotazky = ", mojeotazky)

        if len(finalneotazky) == 0:
            tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
            engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 10;")
            omg = 1
            result_set = engine.fetchall()
            for r in result_set:
                x = random.choice(r[:1])
                y = random.choice(r[1:])
                tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                tabulkovydic['tabulka' + str(omg) + 'body'] = y
                omg += 1

            respond = make_response(render_template('layout.html', control='Nemame otazky', bdy=body, sklonovanie=koncovka,
                                                    tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                                    tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body']))
            return respond

        else:
            ypsilon = random.choice(finalneotazky)
            print('vypise pole po castiach nech s nimi moze robit', randommeno, '||', mojeotazky, '||', ypsilon, '||', body, '||', koncovka)
            for otazky in root.findall('otazka'):
                number = otazky.attrib.get('number')
                print('ypsilon: ', ypsilon, 'number: ', number)
                if str(ypsilon) == number:
                    ot = otazky.find('ot').text
                    od = otazky.find('od').text
                    ma = otazky.find('ma').text
                    mb = otazky.find('mb').text
                    mc = otazky.find('mc').text
                    md = otazky.find('md').text
                    me = otazky.find('me').text
                    mf = otazky.find('mf').text
                    mg = otazky.find('mg').text
                    mh = otazky.find('mh').text
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka)

                    tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
                    result_set = engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 10;")
                    omg = 1
                    result_set = engine.fetchall()
                    for r in result_set:
                        x = random.choice(r[:1])
                        y = random.choice(r[1:])
                        tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                        tabulkovydic['tabulka' + str(omg) + 'body'] = y
                        omg += 1

                    respond = make_response(render_template('layout.html', otazka=ot, ma=ma, mb=mb, mc=mc, md=md, me=me, mf=mf, mg=mg, mh=mh, control=('Spravna odpoved je', od), bdy=body, sklonovanie=koncovka,
                                                            tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                                            tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body']))
                    respond.set_cookie('nameID', json.dumps(pole))
                    return respond


    if request.form['btn'] == 'Kontrola':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]

        polevsetkychotazok = set(list(range(1, 500 + 1)))
        mojeotazky = random.choice(list(pole[1:2]))
        polesplnenychotazok = set(mojeotazky)
        finalneotazky = list(polevsetkychotazok - polesplnenychotazok)

        y = str(pole[2:3])
        ypsilon = y[1:-1]
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]

        for otazky in root.findall('otazka'):
            number = otazky.attrib.get('number')
            print('ypsilon: ', ypsilon, 'number: ', number)
            if str(ypsilon) == number:
                ot = otazky.find('ot').text
                od = otazky.find('od').text

                kont()
                lst = str(od).split(',')
                print('moja', moja, 'od', lst)

                if list(moja) == lst:

                    moja[:] = []
                    mojeotazky.append(int(ypsilon))
                    body = len(mojeotazky)
                    if body == 1:
                        koncovka = 'ku'
                    elif body == 2 or body == 3 or body == 4:
                        koncovka = 'ky'
                    elif body >= 5:
                        koncovka = 'ok'
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka)
                    print('toto vypise pole', pole)

                    jozo = """UPDATE FIIT SET body= %s WHERE uuia4= %s ;"""
                    engine.execute(jozo, (body, randommeno,))
                    tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
                    engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 10;")
                    omg = 1
                    result_set = engine.fetchall()
                    for r in result_set:
                        x = random.choice(r[:1])
                        y = random.choice(r[1:])
                        tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                        tabulkovydic['tabulka' + str(omg) + 'body'] = y
                        omg += 1

                    respond = make_response(render_template('layout.html', control='Vyborne, spravna odpoved!', bdy=body, sklonovanie=koncovka,
                                                            tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                                            tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body']))
                    respond.set_cookie('nameID', json.dumps(pole))
                    return respond

                else:
                    moja[:] = []

                    tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
                    engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 10;")
                    omg = 1
                    result_set = engine.fetchall()
                    for r in result_set:
                        x = random.choice(r[:1])
                        y = random.choice(r[1:])
                        tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                        tabulkovydic['tabulka' + str(omg) + 'body'] = y
                        omg += 1

                    return flask.render_template('layout.html', control='Bohužiaľ nesprávne.', otazka=ot, odp=od, bdy=body, sklonovanie=koncovka,
                                                tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                                tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'])

    if request.form['btn'] == 'Resetuje otazky':
        starekokie = request.cookies.get('nameID')
        starepole = json.loads(starekokie)
        staremeno = str(starepole[:1])
        starerandommeno = staremeno[2:-2]

        staryjozo = """DELETE FROM FIIT WHERE uuia4 = %s ;"""
        engine.execute(staryjozo, (starerandommeno, ))

        randommeno = str(uuid.uuid4())
        mojeotazky = []
        ypsilon = 0
        body = 0
        koncovka = 'ok'

        pole = (randommeno, mojeotazky, ypsilon, body, koncovka)
        print('toto vypise kookie noveho uzivatela', pole)

        jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
        engine.execute(jozo, (randommeno, body))

        tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
        engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 10;")
        omg = 1
        result_set = engine.fetchall()
        for r in result_set:
            x = random.choice(r[:1])
            y = random.choice(r[1:])
            tabulkovydic['tabulka' + str(omg) + 'meno'] = x
            tabulkovydic['tabulka' + str(omg) + 'body'] = y
            omg += 1

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka,
                                                tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                                tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body']))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'Pridat meno':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]

        zadanemeno = request.form['vloztemeno']
        print("randommeno =", randommeno, "|| zadanemeno = ", zadanemeno, "|| body =", body)

        jozo = """UPDATE FIIT SET meno= %s WHERE uuia4= %s ;"""
        engine.execute(jozo, (zadanemeno, randommeno))
        fero = """UPDATE FIIT SET stav= '1' WHERE uuia4= %s ;"""
        engine.execute(fero, (randommeno,))

        tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
        engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 10;")
        omg = 1
        result_set = engine.fetchall()
        for r in result_set:
            x = random.choice(r[:1])
            y = random.choice(r[1:])
            tabulkovydic['tabulka' + str(omg) + 'meno'] = x
            tabulkovydic['tabulka' + str(omg) + 'body'] = y
            omg += 1

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka,
                                                tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                                tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body']))
        return respond


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
