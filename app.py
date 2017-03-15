from flask import Flask, request, render_template, make_response
import flask.views
import random
import xml.etree.ElementTree as ET
import json
import uuid

app = Flask(__name__)

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
    if request.cookies.get('nameID') == None:
        randommeno = str(uuid.uuid4())
        mojeotazky = list(range(1, 5 + 1))
        ypsilon = 0
        body = 0
        koncovka = 'ok'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka)
        print('toto vypise kookie noveho uzivatela', pole)
        respond = make_response(render_template('layout.html', uvod=True, bdy = body, sklonovanie = koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    else:
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        print('stary uzivatel',pole)
        body = random.choice(list(pole[3:4]))
        konc= str(pole[4:5])
        koncovka = konc[2:-2]
        respond = make_response(render_template('layout.html', uvod=True, bdy = body, sklonovaie = koncovka))
        return respond


@app.route('/', methods=['POST'])
def post():
    if request.form['btn'] == 'Nova otazka':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        mojeotazky = random.choice(list(pole[1:2]))
        body = random.choice(list(pole[3:4]))
        konc= str(pole[4:5])
        koncovka = konc[2:-2]
        
        if len(mojeotazky) == 0:
            respond = make_response(render_template('layout.html', control='Nemame otazky', bdy = body, sklonovanie = koncovka))
            return respond

        else:
            ypsilon = random.choice(mojeotazky)
            print('vypise pole po castiach nech s nimi moze robit',randommeno,'||',mojeotazky,'||',ypsilon,'||',body,'||', koncovka)
            for otazky in root.findall('otazka'):
                number = otazky.attrib.get('number')
                print('ypsilon: ',ypsilon,'number: ',number)
                if str(ypsilon) == number:
                    ot = otazky.find('ot').text
                    od = otazky.find('od').text
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka)
                    respond = make_response(render_template('layout.html', otazka=ot, control=('Spravna odpoved je', od), bdy = body, sklonovanie = koncovka))
                    respond.set_cookie('nameID', json.dumps(pole))
                    return respond

                
    if request.form['btn'] == 'Kontrola':
        kokie = request.cookies.get('nameID')
        pole = json.loads(kokie)
        meno = str(pole[:1])
        randommeno = meno[2:-2]
        mojeotazky = random.choice(list(pole[1:2]))
        y = str(pole[2:3])
        ypsilon = y[1:2]
        body = random.choice(list(pole[3:4]))
        konc= str(pole[4:5])
        koncovka = konc[2:-2]
        
        for otazky in root.findall('otazka'):
            number = otazky.attrib.get('number')
            print('ypsilon: ',ypsilon,'number: ',number)
            if str(ypsilon) == number:
                ot = otazky.find('ot').text
                od = otazky.find('od').text
                
                kont()
                lst = str(od).split(',')
                print('moja', moja, 'od', lst)

                if list(moja) == lst:
                    moja[:] = []
                    mojeotazky.remove(int(ypsilon))
                    body = 5 - len(mojeotazky)
                    if body == 1:
                        koncovka = 'ku'
                    elif body == 2 or body == 3 or body == 4:
                        koncovka = 'ky'
                    elif body >= 5:
                        koncovka = 'ok'
                    pole = (randommeno, mojeotazky, ypsilon, body, koncovka)
                    print('toto vypise pole', pole)
                    respond = make_response(render_template('layout.html', control='Vyborne, spravna odpoved!', bdy = body, sklonovanie = koncovka))
                    respond.set_cookie('nameID', json.dumps(pole))
                    return respond

                else:
                    moja[:] = []
                    return flask.render_template('layout.html', control='Bohužiaľ nesprávne.', otazka=ot, odp=od, bdy = body, sklonovanie = koncovka)
            
    if request.form['btn'] == 'Resetuje otazky':
        randommeno = str(uuid.uuid4())
        print('RANDOMMENO',randommeno)
        mojeotazky = list(range(1, 5 + 1))
        ypsilon = 0
        body = 0
        koncovka = 'ok'
        pole = (randommeno, mojeotazky, ypsilon, body, koncovka)
        print('toto vypise kookie noveho uzivatela', pole)
        respond = make_response(render_template('layout.html', uvod=True, bdy = body, sklonovanie = koncovka))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
