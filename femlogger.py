import csv, os
from datetime import datetime
import time
import femfm
def log():
    kanaal = '2'
    initiele_waarde = ('', datetime.now())
    laatste_liedje_op_kanaal = {x: initiele_waarde for x in femfm.alle_kanalen}

    while True:
        datum = datetime.now().strftime('%Y-%m-%d')
        bestand = f'liedjes_logs_{datum}.csv'
        if not os.path.isfile(bestand):
            with open(bestand, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Artiest", "Titel", "Starttijd", "Eindtijd", "Vrouw?", "Kanaal"])

        try:
            laatste_liedje, eindtijd = laatste_liedje_op_kanaal[kanaal]
            if datetime.now() > eindtijd: # het vorige liedje is nu afgelopen!

                if x := femfm.huidig_liedje_op_radio(kanaal):
                    artiest, titel, starttijd, eindtijd, eindtijd_object = x
                    vrouw = femfm.is_vrouw(artiest)
                    if not laatste_liedje == titel:
                        with open(bestand, 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([artiest, titel, starttijd, eindtijd, vrouw, kanaal])

                        print("Logging ", artiest, titel, starttijd, vrouw, kanaal)
                        laatste_liedje_op_kanaal[kanaal] = titel, eindtijd_object
                else:
                    print(f"Het is nu {datetime.now().strftime('%H:%M:%S')} en er speelt geen liedje op Radio {kanaal}")
                    time.sleep(15)
            else:
                print(f"Het liedje {laatste_liedje} op Radio {kanaal} is al gelogd!")
                time.sleep(15)
            kanaal = femfm.zap_naar(kanaal)
        except Exception as E:
            print(f"Foutje, bedankt! {str(E)}")

if __name__ == '__main__':
    log()