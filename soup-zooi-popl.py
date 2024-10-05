import csv

import requests
from bs4 import BeautifulSoup



years = [str(x) for x in range(2018, 2024)]

output_bestand = 'papers.csv'
# empty file
with open(output_bestand, 'w', newline='') as file:
    pass

conferences_and_links = {
    'ICSE': 'https://conf.researchr.org/program/icse-{year}/program-icse-{year}/?badge=Technical%20Research',
    'POPL': 'https://popl{year_short}.sigplan.org/program/program-POPL-{year}/'
    }

conferences = conferences_and_links.keys()

def soup():
    for conference in conferences:
        for year in years:
            year_short = year[2:4]
            url = conferences_and_links[conference]
            url = url.format(year_short=year_short, year=year)

            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, 'html.parser')

            programmas = soup.find_all("tr", {"class": "hidable"})
            for p in programmas:
                title_tag = p.find_all("strong")
                try:
                    type = p.find_all("div", {"class": "event-type"})[0].contents[0]
                except:
                    type = "unknown"

                title = title_tag[1].text

                # logging_types = {'ICSE': ['Full-paper'],
                #                  'POPL': ['Talk']}
                #
                #
                # if type in logging_types[conference]:

                with open(output_bestand, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([conference, year, title, type])


if __name__ == '__main__':
    soup()