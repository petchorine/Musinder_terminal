import requests
from bs4 import BeautifulSoup
import copy

URL_WIKI = r"https://fr.wikipedia.org/wiki/Les_1001_albums_qu%27il_faut_avoir_%C3%A9cout%C3%A9s_dans_sa_vie"

class Titre:
    titre_album = {}
    def __init__(self, numero, artiste, titre, annee):
        self.numero = numero
        self.artiste = artiste
        self.titre = titre
        self.annee = annee

class PlayList:

    def __init__(self, playlist):
        self.playlist = playlist

    def show_playlist(self):
        print("""
n°   Artiste                        Album                          Annee
==== ============================== ============================== =====
""")
        for album in self.playlist:
            print(album.numero.ljust(4), album.artiste[:30].ljust(30, "."), 
                    album.titre[:27].ljust(30, "."), album.annee.rjust(4))
        print()

class User:

    def __init__(self, pseudo, id, all_albums_by_decade, remaining_playlist, liked_playlist, unliked_playlist):
        self.pseudo = pseudo
        self.id = id
        self.all_albums_by_decade = all_albums_by_decade
        self.remaining_playlist = remaining_playlist
        self.liked_playlist = liked_playlist
        self.unliked_playlist = unliked_playlist
    
    def add_to_liked_list(self, all_albums):
        print("Voici la liste des albums:")
        self.remaining_playlist = copy.copy(all_albums)
        self.all_albums_by_decade.show_playlist()


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

def introduction():
    nbr_albums = get_all_albums(URL_WIKI)[1]
    print("""
                #########################################
                #                                       #
                #         Bienvenue dans MUSINDER       #
                #                  par                  # 
                #               Petchorine              #
                #                                       #
                #########################################
    """)
    print()
    print(f"""
Tu es sur la version Terminal de l'application Musinder.
Tu vas pouvoir tagger les albums que tu aimes bien dans la liste des "1001 albums qu'il faut avoir écouté dans sa vie". 
Cette liste a été publiée à partir de 2006 sous la direction de Robert Dimery.
Elle contient actuellement {nbr_albums} albums.
""")



albums = get_all_albums(URL_WIKI)

all_albums_dico = []

for album in albums[0][0]:
    album_dico = {"numero": album.numero, "artiste": album.artiste ,"titre": album.titre, "annee": album.annee}
    all_albums_dico.append(album_dico)
    

print(all_albums_dico)
# introduction()

# titre1 = all_albums_dico[0]["titre"]
# print(titre1)



