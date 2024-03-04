## Wat is FemFM

FemFM is een project van wetenschapper Felienne Hermans. Het project addresseert de onbalans in man/vrouw-verhouding op de Nederlandse radio. Het project heeft twee onderdelen. 

### FemFM: De meta radio-zender

Het eerste onderdeel van het project is "meta radiozender" FemFm. Live te beluisteren via www.femfm.nl. Het idee is dat de zender begint op een Nederlands station, en doorzapt als je geen vrouw hoort. Als je wel een vrouw hoort, blijf je luisteren tot het einde van het liedje. 
De code die dat regelt, start een Flask webserver, en zit in main.py.

Je kan deze code gebruiken om je eigen meta-zender te maken, bijv altijd doorzappen als U2 opkomt, of iets dat niet Nederlands-talig is, of wat je maar wilt. 

### De data-analyse

De andere helft van het project is code die *ook* de zenders afluistert, maar dan meteen het liedje opslaat in een data-bestand. Zo verzamelden we alle liedjes in tussen 1 en 26 februari. Die data worden ook weer op www.femfm.nl weergegeven om de hsitorische statistieken op te baseren.
Je kan deze data ook zelf downloaden om er je eigen analyse mee te maken, met de ruwe data in /originals, of met de Excelfile. 

