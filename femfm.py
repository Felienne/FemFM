import os
from datetime import datetime, timedelta

import requests
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server = os.getenv('SERVER')


with open("women.txt", 'r') as w:
    vrouwen = w.read().splitlines()

alle_kanalen = ['2', '3', '5', '538', 'Q', 'Sky', '10', 'Veronica']

def nu():
    if server=='Yes':
        return datetime.now() + timedelta(hours=1)  # tijd op de server is een uur later
    else:
        return datetime.now()

def huidig_liedje_op_radio(kanaal):
    header = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    if kanaal == '3':
        url = 'https://www.npo3fm.nl/api/tracks'
    elif kanaal == '538':
        url = "https://graph.talparad.io/?query=%7B%0A%20%20station(slug%3A%20%22radio-538%22)%20%7B%0A%20%20%20%20title%0A%20%20%20%20playouts(profile%3A%20%22%22%2C%20limit%3A%2010)%20%7B%0A%20%20%20%20%20%20broadcastDate%0A%20%20%20%20%20%20track%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20artistName%0A%20%20%20%20%20%20%20%20isrc%0A%20%20%20%20%20%20%20%20images%20%7B%0A%20%20%20%20%20%20%20%20%20%20type%0A%20%20%20%20%20%20%20%20%20%20uri%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20rankings%20%7B%0A%20%20%20%20%20%20%20%20listName%0A%20%20%20%20%20%20%20%20position%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D&variables=%7B%7D"
        header['x-api-key']= 'da2-abza7qpnqbfe5ihpk4jhcslpgy'
    elif kanaal == '10':
        url = "https://graph.talparad.io/?query=%7B%0A%20%20station(slug%3A%20%22radio-10%22)%20%7B%0A%20%20%20%20title%0A%20%20%20%20playouts(profile%3A%20%22%22%2C%20limit%3A%2010)%20%7B%0A%20%20%20%20%20%20broadcastDate%0A%20%20%20%20%20%20track%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20artistName%0A%20%20%20%20%20%20%20%20isrc%0A%20%20%20%20%20%20%20%20images%20%7B%0A%20%20%20%20%20%20%20%20%20%20type%0A%20%20%20%20%20%20%20%20%20%20uri%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20rankings%20%7B%0A%20%20%20%20%20%20%20%20listName%0A%20%20%20%20%20%20%20%20position%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D&variables=%7B%7D"
        header['x-api-key']= 'da2-33lf2avqmrbs3mgi66jogjj5ba'
    elif kanaal == 'Sky':
        url = "https://graph.talparad.io/?query=%7B%0A%20%20station(slug%3A%20%22sky-radio%22)%20%7B%0A%20%20%20%20title%0A%20%20%20%20playouts(profile%3A%20%22%22%2C%20limit%3A%2010)%20%7B%0A%20%20%20%20%20%20broadcastDate%0A%20%20%20%20%20%20track%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20artistName%0A%20%20%20%20%20%20%20%20isrc%0A%20%20%20%20%20%20%20%20images%20%7B%0A%20%20%20%20%20%20%20%20%20%20type%0A%20%20%20%20%20%20%20%20%20%20uri%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20rankings%20%7B%0A%20%20%20%20%20%20%20%20listName%0A%20%20%20%20%20%20%20%20position%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D&variables=%7B%7D"
        header['x-api-key']= 'da2-27bfqtcztfatfp7ef6feqg2wkq'
    elif kanaal == 'Q':
        url = "https://api.qmusic.nl/2.0/tracks/plays?limit=3&_station_id=qmusic_nl"
    elif kanaal == 'Veronica':
        url = 'https://api.radioveronica.nl/api/nowplaying?stationKey=VERONICA'
    else:
        url = f'http://www.nporadio{kanaal}.nl/api/tracks'

    publiek = ['1', '2', '3', '4', '5']
    talpa = ['538', '10', 'Sky']

    r = requests.get(url, verify=False, headers=header)

    if kanaal in publiek:
        liedje = json.loads(r.content)["data"][0]
        starttijd = liedje["startdatetime"]
        eindtijd = liedje["enddatetime"]

        eindtijd_object = datetime.strptime(eindtijd, '%Y-%m-%dT%H:%M:%S')
        if eindtijd_object < nu():
            return None

        return liedje["artist"], liedje["title"], starttijd, eindtijd, eindtijd_object

    elif kanaal in talpa: #helaas pindakaas, niet allemaal dezelde data!
        data = json.loads(r.content)["data"]
        liedje = data['station']['playouts'][0]
        starttijd = liedje["broadcastDate"]
        artiest = liedje['track']['artistName'].title() #for some reason this API give all caps
        titel = liedje['track']['title']

        starttijd_object = datetime.strptime(starttijd, '%Y-%m-%dT%H:%M:%SZ')+timedelta(hours=1)

        #eindtijd wordt niet gegeven dus doe maar 3 mins erop, en ze lopen een uur achter zoals op de server (dit werkt dus waarschijnlijk online zo niet)
        eindtijd_object = starttijd_object + timedelta(minutes=3)
        if eindtijd_object < nu():
            return None

        return artiest, titel, starttijd_object.strftime('%Y-%m-%dT%H:%M:%S'), eindtijd_object.strftime('%Y-%m-%dT%H:%M:%S'), eindtijd_object
    elif kanaal == "Veronica":
        data = json.loads(r.content)
        artiest = data["artist"]
        titel = data['title']
        duur = data["duration"]

        eindtijd_object = datetime.now() + timedelta(seconds=duur)
        if eindtijd_object < nu():
            return None
        return artiest, titel, datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), eindtijd_object.strftime('%Y-%m-%dT%H:%M:%S'), eindtijd_object

    else: # "Q"
        data = json.loads(r.content)
        liedje = data["played_tracks"][0]
        titel = liedje['title']
        artiest = liedje['artist']['name'].title() #for some reason this API give all caps
        starttijd = liedje["played_at"]
        starttijd_object = datetime.strptime(starttijd, '%Y-%m-%dT%H:%M:%S+01:00')

        #eindtijd wordt niet gegeven dus doe maar 3 mins erop
        eindtijd_object = starttijd_object + timedelta(minutes=3)
        if eindtijd_object < nu():
            return None

        return artiest, titel, starttijd_object.strftime('%Y-%m-%dT%H:%M:%S'), eindtijd_object.strftime('%Y-%m-%dT%H:%M:%S'), eindtijd_object

def zap_naar(kanaal):
    huidig_kanaal_index = alle_kanalen.index(kanaal)
    nieuwe_index = (huidig_kanaal_index + 1) % len(alle_kanalen)
    return alle_kanalen[nieuwe_index]


def is_vrouw(artiest):
    return artiest in vrouwen

def genereer_uitvoer(kanaal):
    vrouw = False
    zap = False

    if x := huidig_liedje_op_radio(kanaal):
        artiest, titel, starttijd, eindtijd, eindtijd_object = x
        vrouw = is_vrouw(artiest)

        if not vrouw:
            volgende_kanaal = zap_naar(kanaal)
            zap = True
            tekst = f"Er speelt GEEN vrouw op Radio {kanaal}, maar {artiest}. Zappen maar!"
            wachttijd = "5"
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
        vrouw = None

    return tekst, volgende_kanaal, wachttijd, vrouw, zap
