import requests
from bs4 import BeautifulSoup



class Titre:

    def __init__(self, numero, artiste, titre, annee):
        self.numero = numero
        self.artiste = artiste
        self.titre = titre
        self.annee = annee


class PlayList:

    def __init__(self, all_albums):
        self.all_albums = all_albums

    def show_all_albums(self):
        print("""
n°   Artiste                        Album                          Annee
==== ============================== ============================== =====
""")
        for album in self.all_albums:
            print(album.numero.ljust(4), album.artiste[:30].ljust(30, "."), 
                    album.titre[:27].ljust(30, "."), album.annee.rjust(4))
        print()


class User:

    def __init__(self, pseudo, id, playlist_all_albums, remaining_playlist, liked_playlist, unliked_playlist):
        self.pseudo = pseudo
        self.id = id
        self.playlist_all_albums = playlist_all_albums
        self.remaining_playlist = remaining_playlist
        self.liked_playlist = liked_playlist
        self.unliked_playlist = unliked_playlist
    
    def add_to_liked_list(self, all_albums):
        print("Voici la liste des albums:")
        self.playlist_all_albums.show_all_albums()

        print("Tape le numero de l'album")
        album_choice = int(input(">>> "))
        self.remaining_playlist.append(all_albums[album_choice - 1])
        while True:
            print("Veux-tu ajouter un album ?")
            print(  "1. oui")
            print(  "2. non")
            add_choice = int(input(">>> "))
            
            if add_choice == 1:
                print("Tape le numero de l'album")
                album_choice = int(input(">>> "))
                self.remaining_playlist.append(all_albums[album_choice - 1])
                continue
            
            if add_choice == 2:
                break
        print("Voici la liste des albums que tu aimes")                    
        for album in self.remaining_playlist:
            print(album.numero.ljust(4), album.artiste[:30].ljust(30, "."), 
                    album.titre[:27].ljust(30, "."), album.annee.rjust(4))
        print()



url_wiki = r"https://fr.wikipedia.org/wiki/Les_1001_albums_qu%27il_faut_avoir_%C3%A9cout%C3%A9s_dans_sa_vie"
page = requests.get(url_wiki)
soup = BeautifulSoup(page.content, 'html.parser')

titres_annees = soup.find_all("span", class_="mw-headline")

# range de 1 (annees 1950) à 8 (annees 2020)
for idx in range(1):
    list_wthout_sort = []
    all_albums = []

    # sélectionne tous les tableaux par décénnie précédés par une balise h3
    tab_by_decade = soup.select("h3 + table")[idx]
    # sélectionne chaque ligne dans chaque tableau
    lines_td = tab_by_decade.select("td")

    for line in lines_td:
        # si dans la ligne, une case ne contient pas de lien (None)...
        # alors affiche le contenu (concerne les cases "n° de ligne" et "année")
        if line.a is None:
            line = line.string.strip()
        # sinon affiche le titre du lien
        else:
            line = line.a.get("title")

        # tableau contenant toutes les lines
        list_wthout_sort.append(line)

    # fonction permettant de créer des sous-listes de 4 éléments (n° de la ligne, auteur, titre, année)
    lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    list_decade = lol(list_wthout_sort, 4)
   
    for album_line in list_decade:
        numero, artiste, titre, annee = album_line
        all_albums.append(Titre(numero, artiste, titre, annee))


sorted_list = []
playlist_all_albums = PlayList(all_albums)        
# all_albums.show_all_albums()


petchorine = User("Petchorine", 1, playlist_all_albums, remaining_playlist=[], liked_playlist=[], unliked_playlist=[])
# petchorine.all_albums.show_all_albums()

petchorine.add_to_liked_list(all_albums)




