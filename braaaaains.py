import musicbrainzngs
import csv
import os

musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/felienne/femfm/",
)

with open('to_classify_until_feb_10.csv', encoding='utf-8-sig', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    headers = next(reader)
    data = [{h: x for (h, x) in zip(headers, row)} for row in reader]

# write headers
output_bestand = 'to_classify_with_percentage.csv'
if not os.path.isfile(output_bestand):
    with open(output_bestand, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Artiest", "Gender", "Group", "Percentage", "Classification"])
        already_saved =[]
else:
    # gather files already in output
    with open('to_classify_with_percentage.csv', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(reader)

        all_data = [{h: x for (h, x) in zip(headers, row)} for row in reader]
        already_saved = [r['Artiest'] for r in all_data]

def save_artiest(output_bestand, artiest, gender, percentage, type):
    with open(output_bestand, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([artiest, gender, percentage, type, 'MusicBrainz'])

i = 0
for record in data:
    artiest = record['Artiest']
    if not artiest in already_saved:
        try:
            print(str(round(i/(len(data)-len(already_saved))*100,2))+"%")
            i += 1
            brain_artist_matches = musicbrainzngs.search_artists(artiest)
            brain_artist_matches = brain_artist_matches['artist-list']

            # simply fetch the first (best?) match
            if type(brain_artist_matches) is list:
                brain_artist = brain_artist_matches[0] #guessing it is not always a list?
            else:
                brain_artist = brain_artist_matches
            artist_type = brain_artist.get('type', 'Group')

            seperation_symbols = ['&', 'Ft', 'ft', '/', '|', 'Feat. ', 'Feat ', 'Featuring', 'featuring']
            ft_present = any([x in artiest for x in seperation_symbols])

            #change this if to any!!
            if ft_present:
                for s in seperation_symbols:
                    if s in artiest:
                        artiest = artiest.split(s)[0]
                save_artiest(output_bestand, record["Artiest"], "?", '0', 'Featuring')

            elif artist_type == 'Group':

                members = musicbrainzngs.get_artist_by_id(brain_artist['id'], includes=['artist-rels'])
                members = [m for m in members['artist']['artist-relation-list'] if m['type'] == 'member of band']
                # there can be a key error: KeyError: 'artist-relation-list'

                women = 0
                for m in members:
                    member_id = m['target']
                    member = musicbrainzngs.get_artist_by_id(member_id)
                    gender = member['artist'].get('gender', '?')
                    if gender == 'Female':
                        women += 1

                gender_string = ''
                if women == len(members):
                    gender_string = 'Vrouw'
                elif women == 0:
                    gender_string = 'Man'
                else:
                    gender_string = 'Mix'

                record['Gender'] = gender_string
                record['Percentage'] = '0' if len(members) == 0 else str(100*women/len(members))
                record['Type'] = 'Group'
                save_artiest(output_bestand, record["Artiest"], record["Gender"], record['Percentage'], record["Type"])
            elif artist_type == 'Person':
                record['Type'] = 'Person'
                artist_gender = brain_artist.get('gender', '?')
                if artist_gender == 'male':
                    record['Gender'] = 'Man'
                elif artist_gender == 'female':
                    record['Gender'] = 'Vrouw'
                elif artist_gender == '?':
                    record['Gender'] = '?'
                save_artiest(output_bestand, record["Artiest"], record["Gender"], '0', record["Type"])
        except Exception as E:
            save_artiest(output_bestand, record["Artiest"], "?", '0',f"Error{str(E)}")
#notes:
# Ezra Glatt is geen vrouw!!!
# maar Julia Sabaté is geen man?!