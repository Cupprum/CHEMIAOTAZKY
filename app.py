# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, make_response
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
def skusaG():
    if request.cookies.get('nameID') is None:
        randommeno = str(uuid.uuid4())
        mojeotazky = []
        ypsilon = 0
        body = 0
        koncovka = 'ok'
        zleotazky = []
        najmensiaotazka = 1
        najvacsiaotazka = 500
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)
        print('toto vypise kookie noveho uzivatela', pole)

        jozo = """INSERT INTO fiit (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
        engine.execute(jozo, (randommeno, body))

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    else:
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        print('stary uzivatel', pole)
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        print(koncovka)

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        return respond


@app.route('/', methods=['POST'])
def skusaP():
    if request.form['btn'] == 'Nová otázka':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        mensiaotazka = random.choice(list(pole[6:7]))
        vacsiaotazka = random.choice(list(pole[7:8]))
        najmensiaotazka = int(mensiaotazka)
        najvacsiaotazka = int(vacsiaotazka)
        print('cudneotazkyprvaposledna', najmensiaotazka, najvacsiaotazka)
        polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))
        mojeotazky = random.choice(list(pole[1:2]))
        polesplnenychotazok = set(mojeotazky)
        finalneotazky = list(polevsetkychotazok - polesplnenychotazok)

        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        zleotazky = random.choice(list(pole[5:6]))
        print("zleotazky = ", zleotazky)

        if len(finalneotazky) == 0:
            respond = make_response(render_template('layout.html', control='Nemame otazky', bdy=body, sklonovanie=koncovka))
            return respond

        else:
            ypsilon = random.choice(finalneotazky)
            print('vypise pole po castiach nech s nimi moze robit', randommeno, '||', mojeotazky, '||', ypsilon, '||', body, '||', koncovka, '||', zleotazky)
            for otazky in root.findall('otazka'):
                number = otazky.attrib.get('number')
                if str(ypsilon) == number:
                    print('ypsilon: ', ypsilon, 'number: ', number)
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
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)

                    respond = make_response(render_template('layout.html', otazka=ot, ma=ma, mb=mb, mc=mc, md=md, me=me, mf=mf, mg=mg, mh=mh,
                                            control=('Spravna odpoved je', od), bdy=body, sklonovanie=koncovka))
                    respond.set_cookie('nameID', json.dumps(pole))
                    return respond

    if request.form['btn'] == 'Kontrola':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        y = str(pole[2:3])
        ypsilon = y[1:-1]
        print('ypsilon', ypsilon)
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]

        if ypsilon == '0':
            respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka, control='Ako chceš odpovedať na otázku ktorú nemáš?'))
            return respond

        else:
            meno = str(pole[:1])
            randommeno = meno[2:-2]
            najmensiaotazka = random.choice(list(pole[6:7]))
            najvacsiaotazka = random.choice(list(pole[7:8]))
            polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))
            mojeotazky = random.choice(list(pole[1:2]))
            polesplnenychotazok = set(mojeotazky)
            finalneotazky = list(polevsetkychotazok - polesplnenychotazok)
            zleotazky = random.choice(list(pole[5:6]))

            for otazky in root.findall('otazka'):
                number = otazky.attrib.get('number')
                if str(ypsilon) == number:
                    print('ypsilon: ', ypsilon, 'number: ', number)
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
                        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)
                        print('toto vypise pole', pole)

                        jozo = """UPDATE FIIT SET body= %s WHERE uuia4= %s ;"""
                        engine.execute(jozo, (body, randommeno,))

                        respond = make_response(render_template('layout.html', control='Vyborne, spravna odpoved!', bdy=body, sklonovanie=koncovka))
                        respond.set_cookie('nameID', json.dumps(pole))
                        return respond

                    else:
                        moja[:] = []
                        zleotazky.append(int(ypsilon))
                        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)
                        respond = make_response(render_template('layout.html', control='Bohužiaľ nesprávne.', otazka=ot, odp=od,
                                                    ma=ma, mb=mb, mc=mc, md=md, me=me, mf=mf, mg=mg, mh=mh, bdy=body,
                                                    sklonovanie=koncovka))
                        respond.set_cookie('nameID', json.dumps(pole))
                        return respond

    if request.form['btn'] == 'Resetuje otázky':
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
        zleotazky = []
        najmensiaotazka = random.choice(list(pole[6:7]))
        najvacsiaotazka = random.choice(list(pole[7:8]))

        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)
        print('toto vypise kookie noveho uzivatela', pole)

        jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
        engine.execute(jozo, (randommeno, body))

        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'Tabulka najlepších':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        najmensiaotazka = random.choice(list(pole[6:7]))
        najvacsiaotazka = random.choice(list(pole[7:8]))
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]

        tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
        engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 0;")
        omg = 1
        result_set = engine.fetchall()
        for r in result_set:
            x = random.choice(r[:1])
            y = random.choice(r[1:])
            tabulkovydic['tabulka' + str(omg) + 'meno'] = x
            tabulkovydic['tabulka' + str(omg) + 'body'] = y
            omg += 1

        respond = make_response(render_template('tabulkanajlpesich.html', otazka="Tvoje meno bolo uložené.", bdy=body, sklonovanie=koncovka,
                                #tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                #tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                #tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                #tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                #tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']
                                ))
        return respond

    if request.form['btn'] == 'Pridať meno':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        najmensiaotazka = random.choice(list(pole[6:7]))
        najvacsiaotazka = random.choice(list(pole[7:8]))
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]

        zadanemeno = request.form['vloztemeno']
        if zadanemeno == "" or zadanemeno == " ":
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
                print('meno este nebolo pouzite')
                print("randommeno =", randommeno, "|| zadanemeno = ", zadanemeno, "|| body =", body)

                jozo = """UPDATE FIIT SET meno= %s WHERE uuia4= %s ;"""
                engine.execute(jozo, (zadanemeno, randommeno))
                fero = """UPDATE FIIT SET stav= '1' WHERE uuia4= %s ;"""
                engine.execute(fero, (randommeno,))

                tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
                engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 0;")
                omg = 1
                result_set = engine.fetchall()
                for r in result_set:
                    x = random.choice(r[:1])
                    y = random.choice(r[1:])
                    tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                    tabulkovydic['tabulka' + str(omg) + 'body'] = y
                    omg += 1

                respond = make_response(render_template('tabulkanajlpesich.html', otazka="Tvoje meno bolo uložené.", bdy=body, sklonovanie=koncovka,
                                        #tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                        #tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                        #tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                        #tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                        #tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']
                                        ))
                return respond

            else:
                tabulkovydic = {'tabulka1meno': None, 'tabulka1body': None, 'tabulka2meno': None, 'tabulka2body': None}
                engine.execute("SELECT meno, body FROM FIIT WHERE stav = '1' ORDER BY body DESC LIMIT 0;")
                omg = 1
                result_set = engine.fetchall()
                for r in result_set:
                    x = random.choice(r[:1])
                    y = random.choice(r[1:])
                    tabulkovydic['tabulka' + str(omg) + 'meno'] = x
                    tabulkovydic['tabulka' + str(omg) + 'body'] = y
                    omg += 1

                respond = make_response(render_template('tabulkanajlpesich.html', otazka="Toto meno bolo už použité, skús iné.", bdy=body, sklonovanie=koncovka,
                                        #tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                        #tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                        #tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                        #tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                        #tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']
                                        ))
                return respond

    if request.form['btn'] == 'Zle zodpovedané otázky':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        najmensiaotazka = random.choice(list(pole[6:7]))
        najvacsiaotazka = random.choice(list(pole[7:8]))

        polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))

        mojeotazky = random.choice(list(pole[1:2]))

        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        zleotazky = random.choice(list(pole[5:6]))
        print("zleotazky = ", zleotazky)

        if len(zleotazky) == 0:
            respond = make_response(render_template('zleotazky.html', otazka="Na všetky otázky si odpovedal dobre, nemáš si čo opraviť"))
            return respond

        else:
            ypsilon = random.choice(zleotazky)
            for otazky in root.findall('otazka'):
                number = otazky.attrib.get('number')
                if str(ypsilon) == number:
                    print('vypise pole po castiach nech s nimi moze robit', randommeno, '||', mojeotazky, '||', ypsilon, '||', zleotazky)
                    print('ypsilon Zle otazky: ', ypsilon, 'number: ', number)
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
                    respond = make_response(render_template('zleotazky.html', otazka=ot, ma=ma, mb=mb, mc=mc, md=md, me=me, mf=mf, mg=mg, mh=mh,
                                                    control=('Spravna odpoved je', od), zleotazky=zleotazky, cislozlejotazky=ypsilon))
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)
                    respond.set_cookie('nameID', json.dumps(pole))
                    return respond

    if request.form['btn'] == 'Ďalšia zlá otázka':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        najmensiaotazka = random.choice(list(pole[6:7]))
        najvacsiaotazka = random.choice(list(pole[7:8]))

        mojeotazky = random.choice(list(pole[1:2]))
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        zleotazky = random.choice(list(pole[5:6]))
        print("zleotazky = ", zleotazky)

        if len(zleotazky) == 0:
            respond = make_response(render_template('zleotazky.html', otazka="Na všetky otázky si odpovedal dobre, nemáš si čo opraviť"))
            return respond

        else:
            ypsilon = random.choice(zleotazky)
            for otazky in root.findall('otazka'):
                number = otazky.attrib.get('number')
                if str(ypsilon) == number:
                    print('vypise pole po castiach nech s nimi moze robit', randommeno, '||', mojeotazky, '||', ypsilon, '||', zleotazky)
                    print('ypsilon Zle otazky: ', ypsilon, 'number: ', number)
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
                    respond = make_response(render_template('zleotazky.html', otazka=ot, ma=ma, mb=mb, mc=mc, md=md, me=me, mf=mf, mg=mg, mh=mh,
                                                    control=('Spravna odpoved je', od), zleotazky=zleotazky, cislozlejotazky=ypsilon))
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)
                    respond.set_cookie('nameID', json.dumps(pole))
                    return respond

    if request.form['btn'] == 'Kontrola zlej otázky':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        najmensiaotazka = random.choice(list(pole[6:7]))
        najvacsiaotazka = random.choice(list(pole[7:8]))

        mojeotazky = random.choice(list(pole[1:2]))

        y = str(pole[2:3])
        ypsilon = y[1:-1]
        print('ypsilon kontrola zlej otazky: ', ypsilon)
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        zleotazky = random.choice(list(pole[5:6]))

        print('vypise pole po castiach nech s nimi moze robit', randommeno, '||', mojeotazky, '||', ypsilon, '||', zleotazky)
        for otazky in root.findall('otazka'):
            number = otazky.attrib.get('number')
            if str(ypsilon) == number:
                print('ypsilon: ', ypsilon, 'number: ', number)
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

                kont()
                lst = str(od).split(',')
                print('moja', moja, 'od', lst)

                if list(moja) == lst:
                    moja[:] = []
                    zleotazky.remove(int(ypsilon))
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)
                    print('toto vypise pole', pole)

                    respond = make_response(render_template('zleotazky.html', control='Vyborne, spravna odpoved!', zleotazky=zleotazky))
                    respond.set_cookie('nameID', json.dumps(pole))
                    return respond

                else:
                    moja[:] = []
                    respond = make_response(render_template('zleotazky.html', control='Bohužiaľ nesprávne.', otazka=ot, odp=od,
                                            ma=ma, mb=mb, mc=mc, md=md, me=me, mf=mf, mg=mg, mh=mh, zleotazky=zleotazky))
                    return respond

    if request.form['btn'] == 'Zmena skúšaných otázok':
        respond = make_response(render_template('ktoreotazky.html'))
        return respond

    if request.form['btn'] == 'Pridať rozmedzie otázok':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        mojeotazky = random.choice(list(pole[1:2]))
        y = str(pole[2:3])
        ypsilon = y[1:-1]
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        zleotazky = random.choice(list(pole[5:6]))

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
                pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka)
                respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
                respond.set_cookie('nameID', json.dumps(pole))
                return respond

    if request.form['btn'] == 'Späť na hlavnú stránku':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        return respond


app.secret_key = os.environ["SESSION_KEY"]

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
