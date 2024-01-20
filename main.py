import requests
import json
from flask import redirect, url_for, render_template

with open("women.txt", 'r') as w:
    vrouwen = w.read().splitlines()

data = {
    'Maximaal aantal zaps'  : 0,
    'Aantal vrouwen gehoord': 0,
    'Aantal mannen gehoord' : 0,
}


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
    return liedje["artist"], liedje["title"]

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
    artiest, titel = huidig_liedje_op_radio(kanaal)
    if not is_vrouw(artiest):
        volgende_kanaal = zap(kanaal)
        tekst = f"Er speelt GEEN vrouw op Radio {kanaal}, maar {artiest}. Zappen maar! Zappen naar Radio {volgende_kanaal}"
        wachttijd = "5"
    else:
        tekst = f"Er speelt een vrouw op Radio {kanaal}! Namelijk {artiest} met {titel}"
        wachttijd = "60"
        volgende_kanaal = kanaal
    return tekst, volgende_kanaal, wachttijd

# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    return redirect(url_for("nu_op", kanaal=2))

# A welcome message to test our server
@app.route('/radio/<kanaal>')
def nu_op(kanaal):
    tekst, volgende_kanaal, wachttijd = genereer_uitvoer(kanaal)
    return render_template("nu_op.html",
                    volgende_url=url_for("nu_op", kanaal=volgende_kanaal),
                    tekst=tekst,
                    wachttijd=wachttijd)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)