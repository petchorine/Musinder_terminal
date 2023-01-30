import requests
from bs4 import BeautifulSoup
import sqlite3
import os

URL_WIKI = r"https://fr.wikipedia.org/wiki/Les_1001_albums_qu%27il_faut_avoir_%C3%A9cout%C3%A9s_dans_sa_vie"
PATH_DB = r"c:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\albums_wiki.db"

def albums_database():
    if os.path.exists(PATH_DB):
        pass
    else:
        with sqlite3.connect(PATH_DB) as connexion:
            curseur = connexion.cursor()
            curseur.execute("""CREATE TABLE albums (
                numero INTEGER NOT NULL PRIMARY KEY,
                artiste VARCHAR,
                album VARCHAR,
                annee INTEGER
                );""")      
albums_database()



class Titre:
    titre_album = {}
    def __init__(self, numero, artiste, titre, annee):
        self.numero = int(numero)
        self.artiste = artiste
        self.titre = titre
        self.annee = int(annee)

    # def add_all_albums_in_db(self):
        with sqlite3.connect(PATH_DB) as connexion:
            curseur = connexion.cursor()
            curseur.execute(f"""INSERT INTO albums (artiste) VALUES ("{self.artiste}")
            """)

def get_all_albums(URL_WIKI):
    page = requests.get(URL_WIKI)
    soup = BeautifulSoup(page.content, 'html.parser')

    titres_annees = soup.find_all("span", class_="mw-headline")
    all_albums = []
    nbr_total_album = 0

    for idx1 in range(1, 9):
        for idx2 in range(idx1):        # range de 1 (annees 1950) à 8 (annees 2020)
            list_wthout_sort = []
            all_albums_by_decade = []
            

            tab_by_decade = soup.select("h3 + table")[idx2]
            lines_td = tab_by_decade.select("td")

            for line in lines_td:
                if line.a is None:
                    line = line.string.strip()
                else:
                    line = line.a.get("title")
                list_wthout_sort.append(line)

            lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
            list_decade = lol(list_wthout_sort, 4)
        
            for album_line in list_decade:
                numero, artiste, titre, annee = album_line
                all_albums_by_decade.append(Titre(numero, artiste, titre, annee))

        all_albums.append(all_albums_by_decade)

    for decade in all_albums:
        nbr_total_album += len(decade)
    

    return all_albums, nbr_total_album


# albums = get_all_albums(URL_WIKI)
get_all_albums(URL_WIKI)

all_albums_dico = []

# for album in albums[0][0]:
#     album_dico = {"numero": album.numero, "artiste": album.artiste ,"titre": album.titre, "annee": album.annee}
#     all_albums_dico.append(album_dico)


# for decade in albums[0][0]:
#     print(decade.numero)


# print(all_albums_dico)