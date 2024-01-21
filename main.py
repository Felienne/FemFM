from datetime import datetime

import requests
import json
from flask import redirect, url_for, render_template, session

with open("women.txt", 'r') as w:
    vrouwen = w.read().splitlines()


def alle_liedjes_van_radio(kanaal):
    if kanaal == 3:
        url = 'https://www.npo3fm.nl/api/tracks'
    else:
        url = f'http://www.nporadio{kanaal}.nl/api/tracks'

    r = requests.get(url, verify=False)
    for liedje in json.loads(r.content)["data"]:
        print(liedje["artist"], "-", liedje["title"])

def huidig_liedje_op_radio(kanaal):
    if int(kanaal) == 3:
        url = 'https://www.npo3fm.nl/api/tracks'
    else:
        url = f'http://www.nporadio{kanaal}.nl/api/tracks'

    r = requests.get(url, verify=False)
    liedje = json.loads(r.content)["data"][0]

    eindtijd = liedje["enddatetime"]

    datetime_object = datetime.strptime(eindtijd, '%Y-%m-%dT%H:%M:%S')
    if datetime_object < datetime.now():
        return None

    return liedje["artist"], liedje["title"], datetime_object

def zap(kanaal):
    if kanaal == '2':
        return '3'
    if kanaal == '3':
        return '4'
    if kanaal == '4':
        return '5'
    if kanaal == '5':
        return '2'

    raise Exception("Onbekend station!!")


def is_vrouw(artiest):
    return artiest in vrouwen

def genereer_uitvoer(kanaal):
    stats = session.get('stats')

    if x := huidig_liedje_op_radio(kanaal):
        artiest, titel, eindtijd = x

        if not is_vrouw(artiest):
            volgende_kanaal = zap(kanaal)
            tekst = f"Er speelt GEEN vrouw op Radio {kanaal}, maar {artiest}. Zappen maar!"
            wachttijd = "5"
            stats['Totaal aantal zaps'] += 1
        else:
            tekst = f"Er speelt een vrouw op Radio {kanaal}! Namelijk {artiest} met {titel}. Dit liedje speelt nog tot {eindtijd.strftime('%H:%M:%S')}."
            duur = (eindtijd - datetime.now()).total_seconds()
            wachttijd = str(duur+60)  # de stream loopt een minuutje ofzo achter
            volgende_kanaal = kanaal
    else:
        tekst = f"Er speelt nu geen liedje op {kanaal}. Even wachten nog...!"
        wachttijd = "30"
        volgende_kanaal = kanaal

    # save stats to session
    session['stats'] = stats
    return tekst, volgende_kanaal, wachttijd, stats

def player(kanaal):
    if kanaal == '2':
        return 'https://radioplayer.nporadio.nl/mini-player/radio2/'
    elif kanaal == '3':
        return 'https://radioplayer.nporadio.nl/mini-player/3fm/'
    elif kanaal == '4':
        return 'https://radioplayer.nporadio.nl/mini-player/radio4/'
    elif kanaal == '5':
        return 'https://radioplayer.nporadio.nl/mini-player/radio5/'

# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)
app.config['SECRET_KEY'] = 'GEHEIM!!!!'


# A welcome message to test our server
@app.route('/')
def index():
    session['stats'] = {
        'Maximaal aantal zaps': 0,
        'Aantal vrouwen gehoord': 0,
        'Aantal mannen gehoord': 0,
        'Totaal aantal zaps': 0
    }
    return redirect(url_for("nu_op", kanaal=2))

# A welcome message to test our server
@app.route('/radio/<kanaal>')
def nu_op(kanaal):
    tekst, volgende_kanaal, wachttijd, stats = genereer_uitvoer(kanaal)
    return render_template("nu_op.html",
                    volgende_url=url_for("nu_op", kanaal=volgende_kanaal),
                    tekst=tekst,
                    wachttijd=wachttijd,
                    iframe=player(kanaal),
                    stats=stats)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)