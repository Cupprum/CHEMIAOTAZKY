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
engine.execute("CREATE TABLE IF NOT EXISTS FIIT (uuia4 text, meno text, body int, stav text);")


jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
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
        lastaction = None
        skupinaotazok = None
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        print('toto vypise kookie noveho uzivatela', pole)

        jozo = """INSERT INTO FIIT (uuia4, meno, body, stav) VALUES (%s, NULL, %s, '0');"""
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

        body = random.choice(list(pole[3:4]))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]
        zleotazky = random.choice(list(pole[5:6]))
        print("zleotazky = ", zleotazky)
        lastaction = None
        skupinaotazok = str(random.choice(list(pole[9:10])))
        print('skupinaotazok |||||||', skupinaotazok)

        if skupinaotazok == 'None':
            finalneotazky = list(polevsetkychotazok - polesplnenychotazok)

        elif skupinaotazok == 'atom':
            finalneotazky = list(atom - polesplnenychotazok)
            print('atom', finalneotazky)

        elif skupinaotazok == 'sustavalatok':
            finalneotazky = list(sustavalatok - polesplnenychotazok)
            print('sustavalatok', finalneotazky)

        elif skupinaotazok == 'latky':
            finalneotazky = list(latky - polesplnenychotazok)
            print('latky', finalneotazky)

        elif skupinaotazok == 'psustava':
            finalneotazky = list(psustava - polesplnenychotazok)
            print('psustava', finalneotazky)

        elif skupinaotazok == 'chvazba':
            finalneotazky = list(chvazba - polesplnenychotazok)
            print('chvazba', finalneotazky)

        elif skupinaotazok == 'nazvoslovie':
            finalneotazky = list(nazvoslovie - polesplnenychotazok)
            print('nazvoslovie', finalneotazky)

        elif skupinaotazok == 'veliciny':
            finalneotazky = list(veliciny - polesplnenychotazok)
            print('veliciny', finalneotazky)

        elif skupinaotazok == 'kyszas':
            finalneotazky = list(kyszas - polesplnenychotazok)
            print('kyszas', finalneotazky)

        elif skupinaotazok == 'reakcie':
            finalneotazky = list(reakcie - polesplnenychotazok)
            print('reakcie', finalneotazky)

        elif skupinaotazok == 'rovnovaha':
            finalneotazky = list(rovnovaha - polesplnenychotazok)
            print('rovnovaha', finalneotazky)

        elif skupinaotazok == 'komplexy':
            finalneotazky = list(komplexy - polesplnenychotazok)
            print('komplexy', finalneotazky)

        elif skupinaotazok == 'priklady':
            finalneotazky = list(priklady - polesplnenychotazok)
            print('priklady', finalneotazky)

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
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)

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
        poslednaaction = random.choice(list(pole[8:9]))
        skupinaotazok = random.choice(list(pole[9:10]))
        print('posledna akcia |||||| ', poslednaaction, 'skupinaotazok', skupinaotazok)
        lastaction = 'kontrola'

        if str(ypsilon) == '0':
            respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka, control='Ako chceš odpovedať na otázku ktorú nemáš?'))
            return respond

        elif poslednaaction == 'kontrola':
            respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka, control='Kontrola kontroly.'))
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
                        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
                        print('toto vypise pole', pole)

                        jozo = """UPDATE FIIT SET body= %s WHERE uuia4= %s ;"""
                        engine.execute(jozo, (body, randommeno,))

                        respond = make_response(render_template('layout.html', control='Vyborne, spravna odpoved!', bdy=body, sklonovanie=koncovka))
                        respond.set_cookie('nameID', json.dumps(pole))
                        return respond

                    else:
                        moja[:] = []
                        zleotazky.append(int(ypsilon))
                        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
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
        najmensiaotazka = random.choice(list(starepole[6:7]))
        najvacsiaotazka = random.choice(list(starepole[7:8]))
        lastaction = None
        skupinaotazok = None

        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
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
            print(r)

        respond = make_response(render_template('tabulkanajlpesich.html', otazka="Tvoje meno bolo uložené.", bdy=body, sklonovanie=koncovka,
                                tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']))
        return respond

    if request.form['btn'] == 'Pridať meno':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        najmensiaotazka = random.choice(list(pole[6:7]))
        najvacsiaotazka = random.choice(list(pole[7:8]))
        body = int(random.choice(list(pole[3:4])))
        konc = str(pole[4:5])
        koncovka = konc[2:-2]

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

                respond = make_response(render_template('tabulkanajlpesich.html', otazka="Toto meno bolo už použité, skús iné.", bdy=body, sklonovanie=koncovka,
                                        tabulka1meno=tabulkovydic['tabulka1meno'], tabulka1body=tabulkovydic['tabulka1body'],
                                        tabulka2meno=tabulkovydic['tabulka2meno'], tabulka2body=tabulkovydic['tabulka2body'],
                                        tabulka3meno=tabulkovydic['tabulka3meno'], tabulka3body=tabulkovydic['tabulka3body'],
                                        tabulka4meno=tabulkovydic['tabulka4meno'], tabulka4body=tabulkovydic['tabulka4body'],
                                        tabulka5meno=tabulkovydic['tabulka5meno'], tabulka5body=tabulkovydic['tabulka5body']))
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
        lastaction = None
        skupinaotazok = random.choice(list(pole[9:10]))

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
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
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
        lastaction = None
        skupinaotazok = random.choice(list(pole[9:10]))

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
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
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
        lastaction = None
        skupinaotazok = random.choice(list(pole[9:10]))

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
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
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
                pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
                respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
                respond.set_cookie('nameID', json.dumps(pole))
                return respond

    if request.form['btn'] == 'atom':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'atom'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'sustavalatok':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'sustavalatok'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'latky':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'latky'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'psustava':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'psustava'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'chvazba':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'chvazba'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'nazvoslovie':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        zleotazky = random.choice(list(pole[5:6]))
        lastaction = None
        skupinaotazok = 'nazvoslovie'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'veliciny':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        zleotazky = random.choice(list(pole[5:6]))
        lastaction = None
        skupinaotazok = 'veliciny'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'kyszas':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'kyszas'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'reakcie':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'reakcie'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'rovnovaha':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'rovnovaha'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'komplexy':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'komplexy'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    if request.form['btn'] == 'priklady':
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
        najmensiaotazka = 1
        najvacsiaotazka = 500
        lastaction = None
        skupinaotazok = 'priklady'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka, zleotazky, najmensiaotazka, najvacsiaotazka, lastaction, skupinaotazok)
        respond = make_response(render_template('layout.html', uvod=True, bdy=body, sklonovanie=koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond


app.secret_key = os.environ["SESSION_KEY"]

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
