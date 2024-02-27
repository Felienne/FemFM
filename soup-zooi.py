import csv

import requests
from bs4 import BeautifulSoup

output_bestand = 'programmas.csv'

einde = 25
data = [f'{x:02d}-02-2024' for x in range(1, einde)]

def soup():
    zenders = ['Radio-10', 'Sky-Radio', 'Qmusic', 'Radio-Veronica', 'Radio-538', 'NPO-Radio-2', 'NPO-Radio-3', 'NPO-Radio-5']
    zenders_slug = {
        'Radio-10': '10',
        'Sky-Radio': 'Sky',
        'Qmusic': 'Q',
        'Radio-Veronica' : 'Veronica',
        'Radio-538': '538',
        'NPO-Radio-2': '2',
        'NPO-Radio-3': '3',
        'NPO-Radio-5': '5'
    }
    for zender in zenders:
        for datum in data:
            response = requests.get(f'https://www.oorboekje.nl/{zender}/{datum}#programmering', headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, 'html.parser')

            programmas = soup.find_all("p", {"class": "pgProgTijdEnTitel"})
            i = 0
            for p in programmas:
                programma_string = str(p.contents[0]).strip()
                begintijd, naam_en_omroep = programma_string.split(' ', 1)
                naam, omroep = naam_en_omroep.split(' (') if "(" in naam_en_omroep else [naam_en_omroep, '']
                #print(begintijd, '-', naam, '-', omroep[0:-1])
                if i < len(programmas)-1:
                    volgende_programma_string = str(programmas[i+1].contents[0]).strip()
                    eindtijd, _ = volgende_programma_string.split(' ', 1)
                else:
                    eindtijd = naam[2:7]
                    naam = naam[8:]
                with open(output_bestand, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([datum, begintijd, eindtijd, zender, zenders_slug[zender], naam, omroep[:-1]])
                i += 1


if __name__ == '__main__':
    soup()