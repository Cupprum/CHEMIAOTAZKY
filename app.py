# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, make_response, session, url_for, redirect
import random
import json
import uuid
import psycopg2
import os
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


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
    print(lst)
    maxbodovzaodpoved = len(lst)
    mojbodovzaodpoved = 0

    if 'a' in moja:
        zadana = 'zakliknute'
    else:
        zadana = 'nezakliknute'
    if 'a' in lst and 'a' in moja:
        print('A si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akoma = 'spravne'
    elif 'a' not in moja and 'a' not in lst:
        akoma = 'neutralne'
    else:
        akoma = 'zle'

    if 'b' in moja:
        zadanb = 'zakliknute'
    else:
        zadanb = 'nezakliknute'
    if 'b' in lst and 'b' in moja:
        print('B si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomb = 'spravne'
    elif 'b' not in moja and 'b' not in lst:
        akomb = 'neutralne'
    else:
        akomb = 'zle'

    if 'c' in moja:
        zadanc = 'zakliknute'
    else:
        zadanc = 'nezakliknute'
    if 'c' in lst and 'c' in moja:
        print('C si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomc = 'spravne'
    elif 'c' not in moja and 'c' not in lst:
        akomc = 'neutralne'
    else:
        akomc = 'zle'

    if 'd' in moja:
        zadand = 'zakliknute'
    else:
        zadand = 'nezakliknute'
    if 'd' in lst and 'd' in moja:
        print('D si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomd = 'spravne'
    elif 'd' not in moja and 'd' not in lst:
        akomd = 'neutralne'
    else:
        akomd = 'zle'

    if 'e' in moja:
        zadane = 'zakliknute'
    else:
        zadane = 'nezakliknute'
    if 'e' in lst and 'e' in moja:
        print('E si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akome = 'spravne'
    elif 'e' not in moja and 'e' not in lst:
        akome = 'neutralne'
    else:
        akome = 'zle'

    if 'f' in moja:
        zadanf = 'zakliknute'
    else:
        zadanf = 'nezakliknute'
    if 'f' in lst and 'f' in moja:
        print('F si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomf = 'spravne'
    elif 'f' not in moja and 'f' not in lst:
        akomf = 'neutralne'
    else:
        akomf = 'zle'

    if 'g' in moja:
        zadang = 'zakliknute'
    else:
        zadang = 'nezakliknute'
    if 'g' in lst and 'g' in moja:
        print('G si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomg = 'spravne'
    elif 'g' not in moja and 'g' not in lst:
        akomg = 'neutralne'
    else:
        akomg = 'zle'

    if 'h' in moja:
        zadanh = 'zakliknute'
    else:
        zadanh = 'nezakliknute'
    if 'h' in lst and 'h' in moja:
        print('H si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        akomh = 'spravne'
    elif 'h' not in moja and 'h' not in lst:
        akomh = 'neutralne'
    else:
        akomh = 'zle'

    dlzkamojejodpovede=len(moja)

    return maxbodovzaodpoved, mojbodovzaodpoved, akoma, akomb, akomc, akomd, akome, akomf, akomg, akomh, zadana, zadanb, zadanc, zadand, zadane, zadanf, zadang, zadanh, dlzkamojejodpovede


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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        kokie = session.get('nameID')
        if kokie is None:
            randommeno = str(uuid.uuid4())
            mojeotazky = []
            ypsilon = 0
            body = 0
            koncovka = 'ok'
            zleotazky = []
            najmensiaotazka = 1
            najvacsiaotazka = 1500
            lastaction = None
            skupinaotazok = None
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            print('novy uzivatel')

            jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
            engine.execute(jozo, (randommeno, body))

            respond = make_response(render_template('layout.html', layout=True, uvod=True, bdy=body, sklonovanie=koncovka))
            session['nameID'] = json.dumps(pole)
            return respond

        else:
            try:
                kokie = session['nameID']
                pole = json.loads(kokie)
                print('stary uzivatel', pole)
                randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()
                pracujenaotazke = 0
                novezleotazky = []
                for x in range(len(zleotazky)):
                    novezleotazky.append(zleotazky[pracujenaotazke])
                    pracujenaotazke += 1
                novezleotazky = zleotazky
                pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                        'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                        'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                respond = make_response(render_template('layout.html', layout=True, uvod=True, bdy=pole['body'], sklonovanie=pole['koncovka']))
                return respond

            except TypeError:
                randommeno = str(uuid.uuid4())
                mojeotazky = []
                ypsilon = 0
                body = 0
                koncovka = 'ok'
                zleotazky = []
                najmensiaotazka = 1
                najvacsiaotazka = 1500
                lastaction = None
                skupinaotazok = None
                pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                        'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                        'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                print('novy uzivatel')

                jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
                engine.execute(jozo, (randommeno, body))

                respond = make_response(render_template('layout.html', layout=True, uvod=True, bdy=body, sklonovanie=koncovka))
                session['nameID'] = json.dumps(pole)
                return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'Nová otázka':
            atom = set([1, 10, 12, 14, 15, 16, 17, 18, 18, 20, 21, 22, 23, 24, 26, 27, 39, 51, 57, 58, 59, 60,
                        67, 215, 374, 383, 384, 385])
            sustavalatok = set([2, 3, 5, 6, 11, 13, 53, 56, 62, 94, 95, 96, 97, 111, 112, 121, 124, 125, 126,
                                128])
            latky = set([4, 7, 8, 9, 36, 40, 55, 78, 79, 105, 117, 118, 119, 120, 143, 144, 145, 202, 203, 212,
                        213, 214, 216, 217, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 230, 231, 232,
                        233, 234, 235, 236, 237, 238, 239, 240, 241, 243, 244, 246, 247, 249, 250, 255, 256,
                        258, 259, 262, 264, 265, 266, 267, 268, 271, 273, 274, 275, 277, 278, 279, 282, 283,
                        284, 288, 289, 290, 291, 296, 297, 298, 300, 303, 304, 305, 306, 307, 308, 312, 313,
                        314, 316, 318, 319, 322, 323, 326, 329, 330, 332, 334, 337, 338, 339, 343, 344, 347,
                        380])
            psustava = set([25, 28, 29, 30, 253, 254, 257, 294, 301, 321, 325, 335, 336, 341, 342, 345, 348,
                            349, 350, 352, 353, 355, 356, 357, 358, 359, 360, 362, 367, 371, 372, 373, 375, 376,
                            377, 379, 381])
            chvazba = set([31, 32, 33, 34, 35, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 61, 63, 64, 65,
                           66, 68, 242, 245, 263, 292, 293, 295, 315])
            nazvoslovie = set([52, 54, 70, 147, 148, 149, 150, 151, 152, 153, 154, 155, 211, 229, 248, 261, 270,
                               272, 281, 285, 286, 287, 299, 302, 310, 311, 320, 327, 331, 333])
            veliciny = set([69, 100, 106, 107, 110, 113, 114, 116, 122, 123, 129, 130, 136, 139, 140])
            kyszas = set([71, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
                          98, 99, 102, 103, 104, 108, 109, 276, 280, 317, 351])
            reakcie = set([101, 115, 127, 131, 132, 133, 134, 135, 137, 138, 141, 142, 146, 156, 157, 158, 159,
                           160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176,
                           177, 178, 179, 180, 181, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 204,
                           205, 206, 207, 208, 209, 210, 218, 251, 252, 260, 269, 309, 324, 328, 340, 346, 354])
            rovnovaha = set([182, 183, 184, 185, 186, 187, 188, 189, 190])
            komplexy = set([361, 363, 364, 365, 366, 368, 369, 370, 378, 382])
            priklady = set([386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402,
                            403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419,
                            420, 421, 422, 423, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437,
                            438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454,
                            455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471,
                            472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488,
                            489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500])

            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None
            polesplnenychotazok = set(mojeotazky)
            polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))

            if skupinaotazok == 'atom':
                typotazky = "Atóm"
                finalneotazky = list(atom - polesplnenychotazok)

            elif skupinaotazok == 'sustavalatok':
                typotazky = "Sústava látok"
                finalneotazky = list(sustavalatok - polesplnenychotazok)

            elif skupinaotazok == 'latky':
                typotazky = "Látky"
                finalneotazky = list(latky - polesplnenychotazok)

            elif skupinaotazok == 'psustava':
                typotazky = "Periodická sústava prvkov"
                finalneotazky = list(psustava - polesplnenychotazok)

            elif skupinaotazok == 'chvazba':
                typotazky = "Chemická väzba"
                finalneotazky = list(chvazba - polesplnenychotazok)

            elif skupinaotazok == 'nazvoslovie':
                typotazky = "Názvoslovie"
                finalneotazky = list(nazvoslovie - polesplnenychotazok)

            elif skupinaotazok == 'veliciny':
                typotazky = "Chemické veličiny"
                finalneotazky = list(veliciny - polesplnenychotazok)

            elif skupinaotazok == 'kyszas':
                typotazky = "Kyseliny a zásady"
                finalneotazky = list(kyszas - polesplnenychotazok)

            elif skupinaotazok == 'reakcie':
                typotazky = "Chemické reakcie"
                finalneotazky = list(reakcie - polesplnenychotazok)

            elif skupinaotazok == 'rovnovaha':
                typotazky = "Chemická rovnovaha"
                finalneotazky = list(rovnovaha - polesplnenychotazok)

            elif skupinaotazok == 'komplexy':
                typotazky = "Komplexné zlúčeniny"
                finalneotazky = list(komplexy - polesplnenychotazok)

            elif skupinaotazok == 'priklady':
                typotazky = "Príklady"
                finalneotazky = list(priklady - polesplnenychotazok)

            else:
                typotazky = "Si skúšaný zo všetkých otázok"
                finalneotazky = list(polevsetkychotazok - polesplnenychotazok)

            if len(finalneotazky) == 0:
                respond = make_response(render_template('layout.html', layout=True, moznosti=True, control='Nemame otazky', bdy=body, sklonovanie=koncovka))
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
                    respond = make_response(render_template('layout.html', layout=True, moznosti=True, checkbuttons=True, typotazok=typotazky,
                                                            otazka=otazkyzdatabazy['ot'], bdy=body, sklonovanie=koncovka,
                                                            ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'], me=otazkyzdatabazy['me'],
                                                            mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'], control=('Spravna odpoved je', otazkyzdatabazy['od'])))
                    session['nameID'] = json.dumps(pole)
                    return respond

        elif request.form['btn'] == 'Kontrola':
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

                    maxbodovzaodpoved, mojbodovzaodpoved, akoma, akomb, akomc, akomd, akome, akomf, akomg, akomh, zadana, zadanb, zadanc, zadand, zadane, zadanf, zadang, zadanh, dlzkamojejodpovede = kont(otazkyzdatabazy)
                    lst = str(otazkyzdatabazy['od']).split(',')
                    print('maxbodovzaodpoved:',maxbodovzaodpoved,'mojbodovzaodpoved: ',mojbodovzaodpoved,'moja', moja, 'lst',lst)
                    if maxbodovzaodpoved == mojbodovzaodpoved and moja == lst:
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

                        moja[:] = []

                        respond = make_response(render_template('layout.html', layout=True, moznosti=True, akoma=akoma, akomb=akomb, akomc=akomc, akomd=akomd,
                                                akome=akome, akomf=akomf, akomg=akomg, akomh=akomh, bdy=body, sklonovanie=koncovka,
                                                control='Výborne, správna odpoveď!', otazka=otazkyzdatabazy['ot'], odp=otazkyzdatabazy['od'],
                                                ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'],
                                                me=otazkyzdatabazy['me'], mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'],
                                                zadana=zadana, zadanb=zadanb, zadanc=zadanc, zadand=zadand,
                                                zadane=zadane, zadanf=zadanf, zadang=zadang, zadanh=zadanh))
                        session['nameID'] = json.dumps(pole)
                        return respond

                    else:
                        if int(ypsilon) in zleotazky:
                            pass
                        else:
                            zleotazky.append(int(ypsilon))
                        pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                                'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                                'lastaction': lastaction, 'skupinaotazok': skupinaotazok}

                        moja[:] = []

                        respond = make_response(render_template('layout.html', layout=True, moznosti=True, akoma=akoma, akomb=akomb, akomc=akomc, akomd=akomd,
                                                akome=akome, akomf=akomf, akomg=akomg, akomh=akomh, bdy=body, sklonovanie=koncovka,
                                                control='Bohužiaľ nesprávne.', otazka=otazkyzdatabazy['ot'], odp=otazkyzdatabazy['od'],
                                                ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'],
                                                me=otazkyzdatabazy['me'], mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'],
                                                zadana=zadana, zadanb=zadanb, zadanc=zadanc, zadand=zadand,
                                                zadane=zadane, zadanf=zadanf, zadang=zadang, zadanh=zadanh))
                        session['nameID'] = json.dumps(pole)
                        return respond

        elif request.form['btn'] == 'Resetuje otázky':
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
            najvacsiaotazka = 1500
            lastaction = None
            skupinaotazok = None

            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}

            jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
            engine.execute(jozo, (randommeno, body))

            respond = make_response(render_template('layout.html', layout=True, uvod=True, bdy=body, sklonovanie=koncovka))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Tabuľka najlepších':
            return redirect(url_for('tabulkanajlepsich'))

        elif request.form['btn'] == 'O projekte':
            return redirect(url_for('oprojekte'))

        elif request.form['btn'] == 'Zmena skúšaných otázok':
            return redirect(url_for('zmenaotazok'))

        elif request.form['btn'] == 'Zle zodpovedané otázky':
            return redirect(url_for('zleotazky'))

        # nechapem preco to normalne nefunguje ale ked to dam do route(/) tak to ide

        elif request.form['btn'] == 'Atóm':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'atom'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Sústava látok':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'sustavalatok'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Látky':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'latky'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Periodická sústava prvkov':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'psustava'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Chemická väzba':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'chvazba'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Názvoslovie':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'nazvoslovie'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Chemické veličiny':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'veliciny'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Kyseliny a zásady':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'kyszas'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Chemické reakcie':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'reakcie'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Chemická rovnováha':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'rovnovaha'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Komplexné zlúčeniny':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'komplexy'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Príklady':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            skupinaotazok = 'priklady'
            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
            respond = make_response(redirect(url_for('home')))
            session['nameID'] = json.dumps(pole)
            return respond

        elif request.form['btn'] == 'Pridať rozmedzie otázok':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            mensiaotazka = request.form['najmensiaotazka']
            vacsiaotazka = request.form['najvacsiaotazka']

            if len(mensiaotazka) == 0 or len(vacsiaotazka) == 0:
                respond = make_response(render_template('layout.html', zmenaotazok=True, control='Musíš zadať obe čísla.'))
                return respond

            else:
                najmensiaotazka = int(mensiaotazka)
                najvacsiaotazka = int(vacsiaotazka)

                if najmensiaotazka >= najvacsiaotazka:
                    respond = make_response(render_template('layout.html', zmenaotazok=True, control='Najmenšia otázka musí byť menšia od najväčšej, zároveň si nemôžu byť rovné.'))
                    return respond

                if najmensiaotazka <= 0:
                    respond = make_response(render_template('layout.html', zmenaotazok=True, control='Najmenšia otázka musí byť väčšia ako 0.'))
                    return respond

                if najvacsiaotazka > 1500:
                    respond = make_response(render_template('layout.html', zmenaotazok=True, control='Najväčšia otázka môže byť maximálne 1500.'))
                    return respond

                else:
                    skupinaotazok = None
                    pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                            'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                            'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                    respond = make_response(render_template('layout.html', layout=True, uvod=True, bdy=body, sklonovanie=koncovka))
                    session['nameID'] = json.dumps(pole)
                    return respond

        elif request.form['btn'] == 'Prejsť na otázku':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            polevsetkychotazok = set(list(range(najmensiaotazka, najvacsiaotazka + 1)))
            polesplnenychotazok = set(mojeotazky)
            lastaction = None

            try:
                if int(request.form['cislootazky']) in list(range(1, 1500 + 1)):
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
                        respond = make_response(render_template('layout.html', layout=True, moznosti=True, checkbuttons=True, otazka=otazkyzdatabazy['ot'],
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
                                        bude skusat pismenka :D ale takto to nefunguje :D alebo si zadal cislo vacsie ako 1500, koniec koncou
                                        si retard a ak sa ti nepaci ze ti tu teraz pindam tak v pravo hore mas tlacitko co vyriesi vsetky tvoje problemy""",
                                        bdy=body, sklonovanie=koncovka))
                return respond

        elif request.form['btn'] == 'Potvrdiť.':
            ma = request.form['moznosta']
            mb = request.form['moznostb']
            mc = request.form['moznostc']
            md = request.form['moznostd']
            me = request.form['moznoste']
            mf = request.form['moznostf']
            mg = request.form['moznostg']
            mh = request.form['moznosth']
            print(ma, mb, mc, md, me, mf, mg, mh)
            respond = make_response(render_template('pridanieotazok.html'))
            return respond

        else:
            htmlotazka = request.form['btn']

            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            lastaction = None

            otazkyzdatabazy = {'cislootazky': None, 'ot': None, 'od': None, 'ma': None, 'mb': None,
                               'mc': None, 'md': None, 'me': None, 'mf': None, 'mg': None, 'mh': None}

            htmlotazkalist = htmlotazka.split('.')
            a = random.choice(htmlotazkalist[0:1])
            hladavdatabaze = """SELECT * FROM otazky WHERE cislootazky = %s;"""
            engine.execute(hladavdatabaze, (a,))
            result_set = engine.fetchall()

            for r in result_set:
                vyberazdatabazy(otazkyzdatabazy, r)
                pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                        'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                        'lastaction': lastaction, 'skupinaotazok': skupinaotazok}
                print(pole)
                respond = make_response(render_template('layout.html', layout=True, moznosti=True, checkbuttons=True,
                                                        otazka=otazkyzdatabazy['ot'], bdy=body, sklonovanie=koncovka,
                                                        ma=otazkyzdatabazy['ma'], mb=otazkyzdatabazy['mb'], mc=otazkyzdatabazy['mc'], md=otazkyzdatabazy['md'], me=otazkyzdatabazy['me'],
                                                        mf=otazkyzdatabazy['mf'], mg=otazkyzdatabazy['mg'], mh=otazkyzdatabazy['mh'], control=('Spravna odpoved je', otazkyzdatabazy['od'])))
                session['nameID'] = json.dumps(pole)
                return respond


@app.route('/tabulkanajlepsich', methods=['GET', 'POST'])
def tabulkanajlepsich():
    if request.method == 'GET':
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

        respond = make_response(render_template("layout.html", tabulkanajlepsich=True, bdy=body, sklonovanie=koncovka,
                                tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']))
        return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'Pridať meno':
            randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

            zadanemeno = request.form['vloztemeno']

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
                    respond = make_response(render_template("layout.html", tabulkanajlepsich=True, otazka="Zvoľ iné meno.",
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

                    respond = make_response(render_template("layout.html", tabulkanajlepsich=True, otazka="Tvoje meno bolo uložené.", bdy=body, sklonovanie=koncovka,
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

                    respond = make_response(render_template("layout.html", tabulkanajlepsich=True, otazka="Toto meno bolo už použité, skús zadať iné.",
                                            bdy=body, sklonovanie=koncovka,
                                            tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                            tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                            tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                            tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                            tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']))
                    return respond


@app.route('/oprojekte', methods=('GET', 'POST'))
def oprojekte():
    if request.method == 'GET':
        respond = make_response(render_template('layout.html', oprojekte=True))
        return respond
    else:
        pass


@app.route('/zmenaotazok', methods=('GET', 'POST'))
def zmenaotazok():
    if request.method == 'GET':
        respond = make_response(render_template('layout.html', zmenaotazok=True))
        return respond


@app.route('/zleotazky', methods=('GET', 'POST'))
def zleotazky():
    if request.method == 'GET':
        randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok = rozborcookie()

        lastaction = None
        zleotazky = sorted(zleotazky, key=int)

        if len(zleotazky) == 0:
            respond = make_response(render_template('vsetkyzleotazky.html', control="Na všetky otázky si odpovedal dobre, nemáš si čo opraviť",
                                    bdy=body, sklonovanie=koncovka))
            return respond

        else:
            loopdata = []
            zlaotazkacislo = 0
            otazkyzdatabazy = {}
            for pocetotazok in range(1, len(zleotazky) + 1):
                hladavdatabaze = """SELECT ot FROM otazky WHERE cislootazky = %s;"""
                engine.execute(hladavdatabaze, (zleotazky[zlaotazkacislo],))
                result_set = engine.fetchall()
                for r in result_set:
                    otazkyzdatabazy['otazka' + str(zlaotazkacislo)] = random.choice(r[0:1])
                    if otazkyzdatabazy['otazka' + str(zlaotazkacislo)] in loopdata:
                        pass
                    else:
                        loopdata.append(otazkyzdatabazy['otazka' + str(zlaotazkacislo)])
                        zlaotazkacislo += 1

            pole = {'randommeno': randommeno, 'mojeotazky': mojeotazky, 'ypsilon': ypsilon, 'body': body,
                    'koncovka': koncovka, 'zleotazky': zleotazky, 'najmensiaotazka': najmensiaotazka, 'najvacsiaotazka': najvacsiaotazka,
                    'lastaction': lastaction, 'skupinaotazok': skupinaotazok}

            respond = make_response(render_template('layout.html', zleotazky=True, loopdata=loopdata))
            session['nameID'] = json.dumps(pole)
            return respond


@app.route('/pridatotazku', methods=('GET', 'POST'))
def pridatotazku():
    if request.method == 'GET':
        respond = make_response(render_template('pridanieotazok.html'))
        return respond

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        respond = render_template('login.html')
        session['password'] = None
        return respond
    if request.method == 'POST':
        if request.form['btn'] == 'Submit':
            passcode = request.form['passcode']
            mysecretkey = app.secret_key
            if passcode == mysecretkey:
                respond = redirect(url_for('justadminthings'))
                session['password'] = app.secret_key
                return respond 
            respond = redirect(url_for('home'))
            return respond

@app.route('/justadminthings', methods=['GET', 'POST'])
def justadminthings():
    if request.method == 'GET':
        kookie = session.get('password')
        if kookie == app.secret_key:
            global engine
            pocetotazok = 0
            loopdata = []
            try:
                engine.execute('''SELECT nazov FROM otazky''')
                result_set = engine.fetchall()
                for r in result_set:
                    print(r)
                    r = random.choice(r[0:1])
                    pocetotazok += 1
                    loopdata.append(r)
            except psycopg2.ProgrammingError:
                pass
            respond = render_template('justadminthings.html', loopdata=loopdata)
            return respond
        else:
            respond = redirect(url_for('home'))
            return respond

    elif request.method == 'POST':
        if request.form['btn'] == 'Pridat vsetko z xml':
            url = urlparse(os.environ["DATABASE_URL"])
            db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
            conn = psycopg2.connect(db)
            conn.autocommit = True
            engine = conn.cursor()
            engine.execute("CREATE TABLE IF NOT EXISTS otazky (cislootazky int, ot text, od text, ma text, mb text, mc text, md text, me text, mf text, mg text, mh text);")

            tree = ET.parse('chemia.xml')
            root = tree.getroot()

            ypsilon = 1
            for otazky in root.findall('otazka'):
                number = otazky.attrib.get('number')
                if str(ypsilon) == number:
                    print('ypsilon: ', ypsilon, 'number: ', number)
                    ot = str(otazky.find('ot').text)
                    ot = ot.strip()
                    od = str(otazky.find('od').text)
                    od = od.strip()
                    ma = str(otazky.find('ma').text)
                    ma = ma.strip()
                    mb = str(otazky.find('mb').text)
                    mb = mb.strip()
                    mc = str(otazky.find('mc').text)
                    mc = mc.strip()
                    md = str(otazky.find('md').text)
                    md = md.strip()
                    me = str(otazky.find('me').text)
                    me = me.strip()
                    mf = str(otazky.find('mf').text)
                    mf = mf.strip()
                    mg = str(otazky.find('mg').text)
                    mg = mg.strip()
                    mh = str(otazky.find('mh').text)
                    mh = mh.strip()
                    vklada = """INSERT INTO otazky (cislootazky, ot, od, ma, mb, mc, md, me, mf, mg, mh) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                    engine.execute(vklada, (ypsilon, ot, od, ma, mb, mc, md, me, mf, mg, mh))
                    ypsilon += 1

            respond = render_template('justadminthings.html', cosatodeje='PREPISANE DO DATABAZY')
            return respond

        elif request.form['btn'] == 'Vymazat vsetko z databazy':
            engine.execute('''DELETE FROM otazky''')
            respond = render_template('justadminthings.html', cosatodeje='V DATABAZE SA NIC NENACHADZA')
            return respond

app.secret_key = os.environ["SESSION_KEY"]


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
