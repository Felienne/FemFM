from datetime import datetime, timedelta
import time
import requests
import json
from flask import redirect, url_for, render_template, session

with open("women.txt", 'r') as w:
    vrouwen = w.read().splitlines()

import os

lokaal = os.getenv('LOCAL_HOST')

def alle_liedjes_van_radio(kanaal):
    if kanaal == 3:
        url = 'https://www.npo3fm.nl/api/tracks'
    else:
        url = f'http://www.nporadio{kanaal}.nl/api/tracks'

    header = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    r = requests.get(url, verify=False, headers=header)
    for liedje in json.loads(r.content)["data"]:
        print(liedje["artist"], "-", liedje["title"])

def nu():
    if lokaal: #fetch env var
        return datetime.now()
    else:
        return datetime.now() + timedelta(hours=1)

def huidig_liedje_op_radio(kanaal):
    if kanaal == '3':
        url = 'https://www.npo3fm.nl/api/tracks'
    elif kanaal == '538':
        url = "https://graph.talparad.io/?query=%7B%0A%20%20station(slug%3A%20%22radio-538%22)%20%7B%0A%20%20%20%20title%0A%20%20%20%20playouts(profile%3A%20%22%22%2C%20limit%3A%2010)%20%7B%0A%20%20%20%20%20%20broadcastDate%0A%20%20%20%20%20%20track%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20artistName%0A%20%20%20%20%20%20%20%20isrc%0A%20%20%20%20%20%20%20%20images%20%7B%0A%20%20%20%20%20%20%20%20%20%20type%0A%20%20%20%20%20%20%20%20%20%20uri%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20rankings%20%7B%0A%20%20%20%20%20%20%20%20listName%0A%20%20%20%20%20%20%20%20position%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D&variables=%7B%7D"
    else:
        url = f'http://www.nporadio{kanaal}.nl/api/tracks'

    header = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
              'x-api-key': 'da2-abza7qpnqbfe5ihpk4jhcslpgy'}

    publiek = ['1', '2', '3', '4', '5']

    r = requests.get(url, verify=False, headers=header)

    if kanaal in publiek:
        liedje = json.loads(r.content)["data"][0]
        starttijd = liedje["startdatetime"]
        eindtijd = liedje["enddatetime"]

        eindtijd_object = datetime.strptime(eindtijd, '%Y-%m-%dT%H:%M:%S')
        if eindtijd_object < nu():
            return None

        return liedje["artist"], liedje["title"], starttijd, eindtijd, eindtijd_object
    else: #helaas pindakaas, niet allemaal dezelde data!
        data = json.loads(r.content)["data"]
        liedje = data['station']['playouts'][0]
        starttijd = liedje["broadcastDate"]
        artiest = liedje['track']['artistName']
        titel = liedje['track']['title']

        #eindtijd wordt niet gegeven dus doe maar 3 mins erop, en ze lopen een uur achter zoals op de server (dit werkt dus waarschijnlijk online zo niet)
        eindtijd_object = datetime.strptime(starttijd, '%Y-%m-%dT%H:%M:%SZ') + timedelta(minutes=3) + timedelta(hours=1)
        if eindtijd_object < nu():
            return None

        return artiest, titel, starttijd, str(eindtijd_object), eindtijd_object
def zap(kanaal, publiek=True):
    if publiek:
        if kanaal == '1':
            return '2'
        if kanaal == '2':
            return '3'
        if kanaal == '3':
            return '4'
        if kanaal == '4':
            return '5'
        if kanaal == '5':
            return '1'
        raise Exception("Onbekend station!!")
    else:
        if kanaal == '1':
            return 'Q'
        if kanaal == 'Q':
            return '2'
        if kanaal == '2':
            return '10'
        if kanaal == '10':
            return '538'
        if kanaal == '538':
            return '1'
        raise Exception("Onbekend station!!")


def is_vrouw(artiest):
    return artiest in vrouwen

def genereer_uitvoer(kanaal):
    stats = session.get('stats')
    publiek = False

    if x := huidig_liedje_op_radio(kanaal):
        artiest, titel, starttijd, eindtijd, eindtijd_object = x

        if not is_vrouw(artiest):
            volgende_kanaal = zap(kanaal, publiek)
            tekst = f"Er speelt GEEN vrouw op Radio {kanaal}, maar {artiest}. Zappen maar!"
            wachttijd = "5"
            stats['Totaal aantal zaps'] += 1
        else:
            tekst = f"Er speelt een vrouw op Radio {kanaal}! Namelijk {artiest} met {titel}. " \
                    f"Dit liedje speelt nog tot {eindtijd_object.strftime('%H:%M:%S')} en het is nu {datetime.now().strftime('%H:%M:%S')}."
            duur = (eindtijd_object - datetime.now()).total_seconds()
            wachttijd = str(duur+60)  # de stream loopt een minuutje ofzo achter
            volgende_kanaal = kanaal
    else:
        tekst = f"Het is nu {datetime.now().strftime('%H:%M:%S')} en er speelt geen liedje op Radio {kanaal}. Even wachten nog...!"
        wachttijd = "30"
        volgende_kanaal = kanaal

    # save stats to session
    session['stats'] = stats
    return tekst, volgende_kanaal, wachttijd, stats

def player(kanaal):
    if kanaal == '1':
        return 'https://radioplayer.nporadio.nl/mini-player/radio1/'
    elif kanaal == '2':
        return 'https://radioplayer.nporadio.nl/mini-player/radio2/'
    elif kanaal == '3':
        return 'https://radioplayer.nporadio.nl/mini-player/3fm/'
    elif kanaal == '4':
        return 'https://radioplayer.nporadio.nl/mini-player/radio4/'
    elif kanaal == '5':
        return 'https://radioplayer.nporadio.nl/mini-player/radio5/'
    elif kanaal == '538':
        return 'https://partnerplayer.juke.nl/radio-538-player/stations/stations-radio-538/radio-538?autoplay=true'

# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)
app.config['SECRET_KEY'] = 'GEHEIM!!!!'

import csv



@app.route('/logging')
def log():
    with open('liedjes_logs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Artiest", "Titel", "Starttijd", "Eindtijd", "Vrouw?", "Kanaal"])

    kanaal = '1'
    initiele_waarde = ('', datetime.now())
    laatste_liedje_op_kanaal = {'1': initiele_waarde, '2': initiele_waarde, '3': initiele_waarde, '4':initiele_waarde, '5':initiele_waarde}
    while True:
        laatste_liedje, eindtijd = laatste_liedje_op_kanaal[kanaal]
        if datetime.now() > eindtijd: # het vorige liedje is nu afgelopen!

            if x := huidig_liedje_op_radio(kanaal):
                artiest, titel, starttijd, eindtijd, eindtijd_object = x
                vrouw = is_vrouw(artiest)
                if not laatste_liedje == titel:
                    with open('liedjes_logs.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([artiest, titel, starttijd, eindtijd, vrouw, kanaal])

                    print("Logging ", artiest, titel, starttijd, eindtijd, vrouw, kanaal)
                    laatste_liedje_op_kanaal[kanaal] = titel, eindtijd_object
            else:
                print(f"Het is nu {datetime.now().strftime('%H:%M:%S')} en er speelt geen liedje op Radio {kanaal}")
                time.sleep(10)
        else:
            print(f"Het liedje {laatste_liedje} op Radio {kanaal} is al gelogd!")
            time.sleep(10)
        kanaal = zap(kanaal)

# A welcome message to test our server
@app.route('/')
def index():
    session['stats'] = {
        'Maximaal aantal zaps': 0,
        'Aantal vrouwen gehoord': 0,
        'Aantal mannen gehoord': 0,
        'Totaal aantal zaps': 0
    }
    return redirect(url_for("nu_op", kanaal=1))

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