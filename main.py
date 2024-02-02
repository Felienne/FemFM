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

import csv



# A welcome message to test our server
@app.route('/')
def index():
    return redirect(url_for("nu_op", kanaal=2))

@app.route('/radio/<kanaal>')
def nu_op(kanaal):
    tekst, volgende_kanaal, wachttijd = femfm.genereer_uitvoer(kanaal)
    return render_template("nu_op.html",
                    volgende_url=url_for("nu_op", kanaal=volgende_kanaal),
                    tekst=tekst,
                    wachttijd=wachttijd,
                    iframe=player(kanaal),
                    stats={})

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)