import musicbrainzngs
import csv
import os

musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/felienne/femfm/",
)

input_file = 'to_classify_NA_17_feb_to_26_feb.csv'

with open(input_file, encoding='utf-8-sig', newline='') as csvfile:
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

def save_artiest(output_bestand, artiest, gender, percentage, type, brainz_artist):
    with open(output_bestand, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([artiest, gender, percentage, type, 'MusicBrainz', brainz_artist])

i = 0


def fetch_group(brain_artist):
    record = {}
    members = musicbrainzngs.get_artist_by_id(brain_artist['id'], includes=['artist-rels'])

    try:
        members = [m for m in members['artist']['artist-relation-list'] if m['type'] == 'member of band']
        # there can be a key error: KeyError: 'artist-relation-list'
    except:
        members = []

    women = 0
    for m in members:
        member_id = m['target']
        member = musicbrainzngs.get_artist_by_id(member_id)
        gender = member['artist'].get('gender', '?')
        if gender == 'Female':
            women += 1
    if women == len(members):
        gender_string = 'Vrouw'
    elif women == 0:
        gender_string = 'Man'
    else:
        gender_string = 'Mix'
    record['Gender'] = '?' if len(members) == 0 else gender_string
    record['Percentage'] = '?' if len(members) == 0 else str(100 * women / len(members))
    return record


def fetch_person(brain_artist):
    artist_gender = brain_artist.get('gender', '?')
    if artist_gender == 'male':
        record['Gender'] = 'Man'
    elif artist_gender == 'female':
        record['Gender'] = 'Vrouw'
    elif artist_gender == '?':
        record['Gender'] = '?'
    return record


def fetch_brain_artist(artiest):
    brain_artist_matches = musicbrainzngs.search_artists(artiest)
    brain_artist_matches = brain_artist_matches['artist-list']
    # simply fetch the first (best?) match
    if type(brain_artist_matches) is list:
        brain_artist = brain_artist_matches[0]  # guessing it is not always a list?
    else:
        brain_artist = brain_artist_matches
    return brain_artist

for record in data:
    artiest = record.get('Artiest', None)
    i += 1
    if artiest and artiest not in already_saved:
        try:
            print(str(round(i/(len(data))*100, 2))+"%")

            brain_artist = fetch_brain_artist(artiest)
            artist_type = brain_artist.get('type', 'Group')

            seperation_symbols = ['feat. ', ', ', ' & ', ' X ', 'Ft', 'ft', '/', '|', 'Feat. ', 'Feat ', 'Featuring', 'featuring']
            ft_present = any([x in artiest for x in seperation_symbols])

            if ft_present:
                for s in seperation_symbols:
                    if s in artiest:
                        artiest = artiest.split(s)[0] # fetch 1st artist

                brain_artist = fetch_brain_artist(artiest)
                artist_type = brain_artist.get('type', 'Group')

                if artist_type == 'Group':
                    group = fetch_group(brain_artist)
                    save_artiest(output_bestand, record["Artiest"], group["Gender"], group['Percentage'], 'Featuring-Group',brain_artist['name'])
                elif artist_type == 'Person':
                    person = fetch_person(brain_artist)
                    percentage = 100 if person['Gender'] == 'Vrouw' else 0
                    save_artiest(output_bestand, record["Artiest"], person['Gender'], percentage, 'Featuring-Person', brain_artist['name'])
                else:
                    save_artiest(output_bestand, record["Artiest"], '?', '?', 'Overig', brain_artist['name'])

            elif artist_type == 'Group':
                group = fetch_group(brain_artist)
                save_artiest(output_bestand, artiest, group["Gender"], group['Percentage'], 'Group', brain_artist['name'])

            elif artist_type == 'Person':
                person = fetch_person(brain_artist)
                percentage = 100 if person['Gender'] == 'Vrouw' else 0
                save_artiest(output_bestand, artiest, person["Gender"], percentage, 'Person', brain_artist['name'])

            else:
                save_artiest(output_bestand, record["Artiest"], '?', '0', 'Featuring', brain_artist['name'])

        except Exception as E:
            save_artiest(output_bestand, record["Artiest"], "?", '0',f"Error{str(E)}", '?')
#notes:
# Ezra Glatt is geen vrouw!!!
# maar Julia Sabaté is geen man?!

# Blackbird Blackbird is niet de nederlandse singer singwriter?