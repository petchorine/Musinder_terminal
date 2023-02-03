import sqlite3
import requests
from bs4 import BeautifulSoup

URL_WIKI = r"https://fr.wikipedia.org/wiki/Les_1001_albums_qu%27il_faut_avoir_%C3%A9cout%C3%A9s_dans_sa_vie"

def get_albums_content(URL_WIKI):
    page = requests.get(URL_WIKI)
    soup = BeautifulSoup(page.content, 'html.parser')
    tab_by_decade = soup.select("h3 + table")
    return tab_by_decade

def process_album_content(tab_by_decade):
    all_albums = []
    for idx1 in range(1, 9):
        for idx2 in range(idx1):        
            list_wthout_sort = []
            all_albums_by_decade = []
            lines_td = tab_by_decade[idx2].select("td")

            for line in lines_td:
                if line.a is None:
                    line = line.string.strip()
                else:
                    line = line.a.get("title")
                list_wthout_sort.append(line)

            lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
            list_decade = lol(list_wthout_sort, 4)
        
            for album_line in list_decade:
                index_id, artist, title, year = album_line
                new_entry = {"index_id": index_id, "artist": artist, "title": title, "year": year}
                all_albums_by_decade.append(new_entry)

        all_albums.append(all_albums_by_decade)
    return all_albums

def get_albums(URL_WIKI):
    tab_by_decade = get_albums_content(URL_WIKI)
    all_albums = process_album_content(tab_by_decade)
    nbr_total_album = sum([len(decade) for decade in all_albums])
    return all_albums, nbr_total_album

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

class Album:
    def __init__(self, album_id, artist, title, year):
        self.album_id = album_id
        self.artist = artist
        self.title = title
        self.year = year

class User:
    def __init__(self, username, liste_albums):
        self.username = username
        self.remaining_list = []
        self.liked_list = []
        self.unliked_list = []

        self.conn = sqlite3.connect(fr'C:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V1\{username}_albums.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS remaining_list (album_id text, artist text, title text, year text)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS liked_list (album_id text, artist text, title text, year text)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS unliked_list (album_id text, artist text, title text, year text)''')

        for album in liste_albums:
            self.add_album(album["index_id"], album["artist"], album["title"], album["year"])
        self.conn.commit()

    def add_album(self, album_id, artist, title, year):
        album = Album(album_id, artist, title, year)
        self.remaining_list.append(album)
        self.cursor.execute('''INSERT INTO remaining_list VALUES (?,?,?,?)''', (album_id, artist, title, year))
        self.conn.commit()

    def liked_album(self, album_id):
        flag = False
        for album in self.remaining_list:
            if album.album_id == album_id:
                self.liked_list.append(album)
                self.remaining_list.remove(album)
                flag = True

            if flag:
                self.cursor.execute(f"SELECT * FROM liked_list WHERE album_id='{album_id}'")
                if not self.cursor.fetchone():
                    self.cursor.execute('''INSERT INTO liked_list VALUES (?,?,?,?)''', (album_id, album.artist, album.title, album.year))
                    self.cursor.execute('''DELETE FROM remaining_list WHERE album_id=?''', (album_id,))
                    self.conn.commit()
                    print(f"L'album a été ajouté à liked_list")
                else:
                    print(f"L'album existe déjà dans liked_list")
            else:
                print("L'album n'a pas été trouvé dans la remaining_list")
                
    def unliked_album(self, album_id):
        flag = False
        for album in self.remaining_list:
            if album.album_id == album_id:
                self.unliked_list.append(album)
                self.remaining_list.remove(album)
                flag = True

            if flag:
                self.cursor.execute(f"SELECT * FROM unliked_list WHERE album_id='{album_id}'")
                if not self.cursor.fetchone():
                    self.cursor.execute('''INSERT INTO unliked_list VALUES (?,?,?,?)''', (album_id, album.artist, album.title, album.year))
                    self.cursor.execute('''DELETE FROM remaining_list WHERE album_id=?''', (album_id,))
                    self.conn.commit()
                    print(f"L'album a été ajouté à unliked_list")
                else:
                    print(f"L'album existe déjà dans unliked_list")
            else:
                print("L'album n'a pas été trouvé dans la remaining_list")

    def close(self):
        self.conn.close

def introduction():
    nbr_albums = get_albums(URL_WIKI)[1]
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


# for i in range(len(get_albums(URL_WIKI)[0])):
#     BASE = get_albums(URL_WIKI)[0][i]
#     toto = User("toto", BASE)



introduction()

