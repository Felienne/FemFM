from datetime import datetime, timedelta
import time
import femfm
from flask import redirect, url_for, render_template, session


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
    elif kanaal == 'Sky':
        return 'https://partnerplayer.juke.nl/sky-radio/stations/stations-sky-radio/sky-radio?autoplay=true'
    elif kanaal == '10':
        return 'https://partnerplayer.juke.nl/radio-10/stations/stations-radio-10/radio-10?autoplay=true'
    elif kanaal == 'Veronica':
        return 'https://stream.radioveronica.nl/veronica?dist=nlfm'
    elif kanaal == "Q":
        return 'https://player.qmusic.nl/8AQ5l9gSu7952HphVCOiiyGaCziBKdkR'

# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)
app.config['SECRET_KEY'] = 'GEHEIM!!!!'


@app.route('/')
def index():
    session['stats'] = {
        'Maximaal aantal zaps': 0,
        'Aantal vrouwen gehoord': 0,
        'Aantal mannen gehoord': 0,
        'Totaal aantal zaps': 0
    }
    return redirect(url_for("nu_op", kanaal=2))



@app.route('/radio/<kanaal>')
def nu_op(kanaal):
    stats = session.get('stats')
    if stats is None:
        stats = {
            'Maximaal aantal zaps': 0,
            'Aantal vrouwen gehoord': 0,
            'Aantal mannen gehoord': 0,
            'Totaal aantal zaps': 0
        }

    tekst, volgende_kanaal, wachttijd, vrouw, zap, programma = femfm.genereer_uitvoer(kanaal)

    if vrouw is not None: # geen liedje = None
        if vrouw:
            stats['Aantal vrouwen gehoord'] += 1
            stats['Totaal aantal zaps'] = 0
        else:
            stats['Aantal mannen gehoord'] += 1

    if zap:
        stats['Totaal aantal zaps'] += 1

        if stats['Totaal aantal zaps'] > stats['Maximaal aantal zaps']:
            stats['Maximaal aantal zaps'] = stats['Totaal aantal zaps']

    # save stats back to session

    aantal_liedjes = stats['Aantal mannen gehoord'] + stats['Aantal vrouwen gehoord']
    stats['Percentage'] = 0 if aantal_liedjes == 0 else round(stats['Aantal vrouwen gehoord']/aantal_liedjes*100,1)

    session['stats'] = stats

    return render_template("nu_op.html",
                    volgende_url=url_for("nu_op", kanaal=volgende_kanaal),
                    tekst=tekst,
                    wachttijd=wachttijd,
                    iframe=player(kanaal),
                    stats=stats)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)