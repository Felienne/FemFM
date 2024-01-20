import requests
import json
import time

with open("women.txt", 'r') as w:
    vrouwen = w.readlines()

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
    if kanaal == 3:
        url = 'https://www.npo3fm.nl/api/tracks'
    else:
        url = f'http://www.nporadio{kanaal}.nl/api/tracks'

    r = requests.get(url, verify=False)
    liedje = json.loads(r.content)["data"][0]
    return liedje["artist"], liedje["title"]

def zap(kanaal):
    if kanaal == 2:
        return 3
    if kanaal == 3:
        return 4
    if kanaal == 4:
        return 5
    if kanaal == 5:
        return 2


def is_vrouw(artiest):
    return artiest in vrouwen

# if __name__ == '__main__':
#     kanaal = 2
#     while True:
#         artiest, titel = huidig_liedje_op_radio(kanaal)
#         if not is_vrouw(artiest):
#             print(f"Er speelt GEEN vrouw op Radio {kanaal}, maar {artiest}. Zappen maar!")
#             time.sleep(30)
#             kanaal = zap(kanaal)
#             print(f"Zappen naar Radio {kanaal}")
#         else:
#             print(f"Er speelt een vrouw op Radio {kanaal}! Namelijk {artiest} met {titel}")
#             time.sleep(30)

# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)