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

class User:
    def __init__(self, username, liste_albums):
        self.username = username
        self.db_manager = DatabaseManager(fr'C:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\{username}_albums.db')

        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS remaining_list (album_id text, artist text, title text, year text, decade integer)''')
        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS liked_list (album_id text, artist text, title text, year text, decade integer)''')
        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS unliked_list (album_id text, artist text, title text, year text, decade integer)''')

        for album in liste_albums:
            self.add_album(album["index_id"], album["artist"], album["title"], album["year"], album["decade"])
    
        self.db_manager.connect().commit()

    def add_album(self, album_id, artist, title, year, decade):        
        query1 = "SELECT 1 FROM remaining_list WHERE album_id=? AND artist=? AND title=? AND year=? AND decade=?"
        result1 = self.db_manager.execute_query(query1, (album_id, artist, title, year, decade))
        query2 = "SELECT 1 FROM liked_list WHERE album_id=? AND artist=? AND title=? AND year=? AND decade=?"
        result2 = self.db_manager.execute_query(query2, (album_id, artist, title, year, decade))
        query3 = "SELECT 1 FROM liked_list WHERE album_id=? AND artist=? AND title=? AND year=? AND decade=?"
        result3 = self.db_manager.execute_query(query3, (album_id, artist, title, year, decade))
        
        if result1 or result2 or result3:
            pass
        else:
            insert_query = "INSERT INTO remaining_list VALUES (?,?,?,?,?)"
            self.db_manager.execute_query(insert_query, (album_id, artist, title, year, decade))
            self.db_manager.connect().commit()

    def decade_choice(self):
        choices = [(1, 1950), (2, 1960), (3, 1970), (4, 1980), (5, 1990), (6, 2000), (7, 2010), (8, 2020)]
        print()
        print("Les albums de quelle décennie souhaites-tu voir ? ('q' pour quitter)" )
        print(" 1. 1950")
        print(" 2. 1960")
        print(" 3. 1970")
        print(" 4. 1980")
        print(" 5. 1990")
        print(" 6. 2000")
        print(" 7. 2010")
        print(" 8. 2020")
        while True:
            choice_decade = input(">>> ")      
            try:
                choice_decade_int = int(choice_decade)
                if choice_decade_int in [1, 2, 3, 4, 5, 6, 7, 8]:
                    if self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE decade = {choices[choice_decade_int - 1][1]}'''):
                        self.show_remaining_list(choices[choice_decade_int - 1][1])
                        return choices[choice_decade_int - 1][1]
                    else:
                        print(f"Tous les albums ont été taggés pour les années {choices[choice_decade_int - 1][1]}.") 
                        print()
                        continue
                elif choice_decade_int in [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]:
                    if self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE decade = {choice_decade_int}'''):
                        self.show_remaining_list(choice_decade_int)
                        return choice_decade_int
                    else:
                        print(f"Tous les albums ont été taggés pour les années {choice_decade_int}.") 
                        print()
                        continue
                else:
                    print("Tu dois choisir une des options proposées.")
                    continue
            except:
                if choice_decade == "q":
                    quit()
                else:
                    print("Tu dois choisir une des options proposées.")
                    continue

    def show_remaining_list(self, choice):
        print()
        print(f"Voici les albums qu'il te reste à tagger pour les années {choice}.")
        print("""
n°   Artiste                        Album                          Annee
==== ============================== ============================== =====
""")
        rows = self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE decade = {choice}''')
        for row in rows:
            print(row[0].ljust(4), row[1][:30].ljust(30, "."), 
                    row[2][:27].ljust(30, "."), row[3].rjust(4))

    def add_to_liked_or_unliked(self, decade):
        while self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE decade = {decade}'''):
            print()
            print("Que souhaites-tu faire ?")
            print(" 1. tagger un nouvel album")
            print(f" 2. afficher à nouveau la liste des albums des années {decade}")
            print(" 3. revenir au menu et changer de décennie")
            user_choice = input(">>> ")

            if user_choice == "1":
                print()
                print("Tape le n° de l'album :")
                album_choice = input(">>> ")
                if album_choice.isdecimal():
                    album = self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE album_id = {album_choice}''')
                    if album:
                        print()
                        print(f"As-tu aimé l'album '{album[0][2]}' de {album[0][1]} ?")
                        print(" 1. oui")
                        print(" 2. non")
                        user_choice = input(">>> ")

                        if user_choice == "1":       
                            self.liked_album(album[0][0])
                            continue
                        elif user_choice == "2":
                            self.unliked_album(album[0][0])
                            continue
                        else:
                            print("Tu dois choisir 1 ou 2.")
                            self.add_to_liked_or_unliked()
                    else:
                        print("Cet album n'est pas dans la liste.")
                        continue
                else:
                    print("Tu dois taper le n° de l'album.")
                    continue
            elif user_choice == "2":
                self.show_remaining_list(decade)
            elif user_choice == "3":
                decade = self.decade_choice()
                self.add_to_liked_or_unliked(decade)
            else:
                print("Tu dois choisir entre 1, 2 ou 3.")
                continue

        if not self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE decade = {decade}'''):
            print(f"Tous les albums ont été taggés pour les années {decade}.") 
            decade = self.decade_choice()
            self.add_to_liked_or_unliked(decade)
 
    def liked_album(self, album_id):
        album = self.db_manager.execute_query(f"SELECT * FROM remaining_list WHERE album_id='{album_id}'")
        if album:
            if not self.db_manager.execute_query(f"SELECT * FROM liked_list WHERE album_id='{album_id}'"):
                self.db_manager.execute_query('''INSERT INTO liked_list VALUES (?,?,?,?,?)''', (album[0][0], album[0][1], album[0][2], album[0][3], album[0][4]))
                self.db_manager.execute_query('''DELETE FROM remaining_list WHERE album_id=?''', (album_id,))
                self.db_manager.connect().commit()
                print(f"L'album a été ajouté à liked_list")                
            else:
                print(f"L'album existe déjà dans liked_list")
        else:
            print("L'album n'a pas été trouvé dans la remaining_list")
               
    def unliked_album(self, album_id):
        album = self.db_manager.execute_query(f"SELECT * FROM remaining_list WHERE album_id='{album_id}'")
        if album:
            if not self.db_manager.execute_query(f"SELECT * FROM unliked_list WHERE album_id='{album_id}'"):
                self.db_manager.execute_query('''INSERT INTO unliked_list VALUES (?,?,?,?,?)''', (album[0][0], album[0][1], album[0][2], album[0][3], album[0][4]))
                self.db_manager.execute_query('''DELETE FROM remaining_list WHERE album_id=?''', (album_id,))
                self.db_manager.connect().commit()
                print(f"L'album a été ajouté à unliked_list")                
            else:
                print(f"L'album existe déjà dans unliked_list")
        else:
            print("L'album n'a pas été trouvé dans la remaining_list")

    def close(self):
        self.conn.close

for i in range(len(get_albums(URL_WIKI)[0])):
    BASE = get_albums(URL_WIKI)[0][i]
    toto = User("toto", BASE)

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


introduction()
decade = toto.decade_choice()
toto.add_to_liked_or_unliked(decade)

