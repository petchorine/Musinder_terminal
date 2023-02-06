import sqlite3
import requests
from bs4 import BeautifulSoup
import os

URL_WIKI = r"https://fr.wikipedia.org/wiki/Les_1001_albums_qu%27il_faut_avoir_%C3%A9cout%C3%A9s_dans_sa_vie"

def get_albums_content(URL_WIKI):
    page = requests.get(URL_WIKI)
    soup = BeautifulSoup(page.content, 'html.parser')
    tab_by_decade = soup.select("h3 + table")
    return tab_by_decade

def process_album_content(tab_by_decade):
    all_albums = []
    decade = 1950
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
                new_entry = {"index_id": index_id, "artist": artist, "title": title, "year": year, "decade": decade}
                all_albums_by_decade.append(new_entry)
        all_albums.append(all_albums_by_decade)
        decade += 10   
    return all_albums

def get_albums(URL_WIKI):
    tab_by_decade = get_albums_content(URL_WIKI)
    all_albums = process_album_content(tab_by_decade)
    nbr_total_album = sum([len(decade) for decade in all_albums])
    return all_albums, nbr_total_album

class DatabaseManager:
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db

    def connect(self):
        return sqlite3.connect(self.path_to_db)

    def execute_query(self, query, values=None):
        with self.connect() as connection:
            cursor = connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            return cursor.fetchall()

class Album:
    def __init__(self, album_id, artist, title, year, decade):
        self.album_id = album_id
        self.artist = artist
        self.title = title
        self.year = year
        self.decade = decade

class User:
    def __init__(self, username, liste_albums):
        self.username = username
        self.remaining_list = []
        self.liked_list = []
        self.unliked_list = []
        self.db_manager = DatabaseManager(fr'C:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\{username}_albums.db')

        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS remaining_list (album_id text, artist text, title text, year text, decade integer)''')
        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS liked_list (album_id text, artist text, title text, year text, decade integer)''')
        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS unliked_list (album_id text, artist text, title text, year text, decade integer)''')

        for album in liste_albums:
            self.add_album(album["index_id"], album["artist"], album["title"], album["year"], album["decade"])
    
        self.db_manager.connect().commit()

    def add_album(self, album_id, artist, title, year, decade):        
        album = Album(album_id, artist, title, year, decade)
        self.remaining_list.append(album)
        
        query = "SELECT 1 FROM remaining_list WHERE album_id=? AND artist=? AND title=? AND year=? AND decade=?"
        result = self.db_manager.execute_query(query, (album_id, artist, title, year, decade))
        if result:
            pass
        else:
            insert_query = "INSERT INTO remaining_list VALUES (?,?,?,?,?)"
            self.db_manager.execute_query(insert_query, (album_id, artist, title, year, decade))
            self.db_manager.connect().commit()
                
    def add_to_liked_or_unliked(self):
        while self.remaining_list:
            print()
            print("Que souhaites-tu faire ?")
            print(" 1. tagger un nouvel album")
            print(" 2. afficher les albums qu'il te reste à tagger")
            print(" 3. revenir au menu")
            user_choice = input(">>> ")

            if user_choice == "1":
                print()
                print("Tape le n° de l'album :")
                album_choice = input(">>> ")
                
                for album_present_or_not in self.remaining_list:
                    if album_choice in album_present_or_not.values():
                        print()
                        print("As-tu aimé cet album ?")
                        print(" 1. oui")
                        print(" 2. non")
                        user_choice = input(">>> ")

                        if user_choice == "1":       
                            self.liked_album(user_choice)
                        elif user_choice == "2":
                            self.unliked_album(user_choice)
                        else:
                            print("Tu dois choisir 1 ou 2.")
                            self.add_to_liked_or_unliked()
                    else:
                        print("Cet album n'est pas dans la liste.")
                        break
            elif user_choice == "2":
                self.show_remaining_list()
            elif user_choice == "3":
                print("menu")
                return self.remaining_list, self.liked_list, self.unliked_list
            else:
                print("Tu dois choisir entre 1, 2 ou 3.")
                continue

        print("Tous les albums ont été taggés.") 

    def show_remaining_list(self, choice):
        choices = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]    
        print()
        print("""
n°   Artiste                        Album                          Annee
==== ============================== ============================== =====
""")
                
        rows = self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE decade = {choices[choice - 1]}''')
        for row in rows:
            print(row[0].ljust(4), row[1][:30].ljust(30, "."), 
                    row[2][:27].ljust(30, "."), row[3].rjust(4))

    def liked_album(self, album_id):
        flag = False
        for album in self.remaining_list:
            if album.album_id == album_id:
                self.liked_list.append(album)
                self.remaining_list.remove(album)
                flag = True

            if flag:
                self.db_manager.execute_query(f"SELECT * FROM liked_list WHERE album_id='{album_id}'")
                
                with sqlite3.connect(fr'C:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\{self.username}_albums.db') as connection:
                    cursor = connection.cursor()

                if not cursor.fetchone():
                    self.db_manager.execute_query('''INSERT INTO liked_list VALUES (?,?,?,?,?)''', (album_id, album.artist, album.title, album.year, album.decade))
                    self.db_manager.execute_query('''DELETE FROM remaining_list WHERE album_id=?''', (album_id,))
                    self.db_manager.connect().commit()
                    print(f"L'album a été ajouté à liked_list")
                    break
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
                self.db_manager.execute_query(f"SELECT * FROM unliked_list WHERE album_id='{album_id}'")
                
                with sqlite3.connect(fr'C:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\{self.username}_albums.db') as connection:
                    cursor = connection.cursor()

                if not cursor.fetchone():
                    self.db_manager.execute_query('''INSERT INTO unliked_list VALUES (?,?,?,?,?)''', (album_id, album.artist, album.title, album.year, album.decade))
                    self.db_manager.execute_query('''DELETE FROM remaining_list WHERE album_id=?''', (album_id,))
                    self.db_manager.connect().commit()
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

Les albums de quelle décennie souhaites-tu voir ?
    1. 1950
    2. 1960
    3. 1970
    4. 1980
    5. 1990
    6. 2000
    7. 2010
    8. 2020
""")


for i in range(len(get_albums(URL_WIKI)[0])):
    BASE = get_albums(URL_WIKI)[0][i]
    toto = User("toto", BASE)


introduction()

# permet d'afficher les albums par décenie
# while True:
#     choice_decade = input(">>> ")
#     if choice_decade == "q":
#         break
#     else:
#         choice_decade_int = int(choice_decade)
#         toto.show_remaining_list(choice_decade_int)


# ajoute l'album à liked_list
toto.liked_album("1083")
