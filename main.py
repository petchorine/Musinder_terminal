import sqlite3
import requests
from bs4 import BeautifulSoup
import sys
import re

class DatabaseManager:
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db
        self.url_wiki = r"https://fr.wikipedia.org/wiki/Les_1001_albums_qu%27il_faut_avoir_%C3%A9cout%C3%A9s_dans_sa_vie"
                
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

    def get_albums_content(self):
        page = requests.get(self.url_wiki)
        soup = BeautifulSoup(page.content, 'html.parser')
        tab_by_decade = soup.select("h3 + table")
        return tab_by_decade

    def process_album_content(self, tab_by_decade):
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

    def get_albums(self):
        tab_by_decade = self.get_albums_content()
        all_albums = self.process_album_content(tab_by_decade)
        nbr_total_album = sum([len(decade) for decade in all_albums])
        return all_albums, nbr_total_album

    def add_albums_to_db(self):
        for i in range(len(self.get_albums()[0])):
            BASE = self.get_albums()[0][i]
            for album in BASE:
                query1 = "SELECT 1 FROM remaining_list WHERE album_id=? AND artist=? AND title=? AND year=? AND decade=?"
                result1 = self.execute_query(query1, (album["index_id"], album["artist"], album["title"], album["year"], album["decade"]))
                query2 = "SELECT 1 FROM liked_list WHERE album_id=? AND artist=? AND title=? AND year=? AND decade=?"
                result2 = self.execute_query(query2, (album["index_id"], album["artist"], album["title"], album["year"], album["decade"]))
                query3 = "SELECT 1 FROM liked_list WHERE album_id=? AND artist=? AND title=? AND year=? AND decade=?"
                result3 = self.execute_query(query3, (album["index_id"], album["artist"], album["title"], album["year"], album["decade"]))
                
                if result1 or result2 or result3:
                    pass
                else:
                    insert_query = "INSERT INTO remaining_list VALUES (?,?,?,?,?)"
                    self.execute_query(insert_query, (album["index_id"], album["artist"], album["title"], album["year"], album["decade"]))
                    self.connect().commit()

class User:
    def __init__(self, username):
        self.username = username
        self.db_manager = DatabaseManager(fr'C:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\{username}_albums.db')

        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS remaining_list (album_id text, artist text, title text, year text, decade integer)''')
        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS liked_list (album_id text, artist text, title text, year text, decade integer)''')
        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS unliked_list (album_id text, artist text, title text, year text, decade integer)''')
        self.db_manager.connect().commit()

        self.db_manager.add_albums_to_db()        
        self.main_menu()
    
    def main_menu(self):
        print()
        print("Que veux-tu faire ?")
        print(" 1. voir la liste par décennie des albums que j'ai aimé")
        print(" 2. voir la liste par décennie des albums que je n'ai pas aimé")
        print(" 3. voir la liste par décennie des albums qu'il te reste à tagger")
        print(" 4. quitter")
    
        while True:
            main_menu_choice = int(input(">>> "))
            
            if (main_menu_choice == 1 or main_menu_choice == 2) and isinstance(main_menu_choice, int):
                self.decade_choice(main_menu_choice)
                print()
                print("Tape 'b' pour revenir au menu principal")
                while True:
                    back_to_menu = input(">>> ")
                    if back_to_menu == "b":
                        self.main_menu()
                    else:
                        print("Tu dois taper 'b' pour revenir au menu")                        
            elif main_menu_choice == 3 and isinstance(main_menu_choice, int):
                decade = self.decade_choice(main_menu_choice)
                self.add_to_liked_or_unliked(decade)
                break
            elif main_menu_choice == 4 and isinstance(main_menu_choice, int):
                sys.exit()
            else:
                print("Tu dois choisir entre 1, 2, 3 ou 4")
                continue               

    def decade_choice(self, main_menu_choice=None):
        list_to_show = ["liked_list", "unliked_list", "remaining_list"]
        choices = [(1, 1950), (2, 1960), (3, 1970), (4, 1980), (5, 1990), (6, 2000), (7, 2010), (8, 2020)]
        print()
        print("Les albums de quelle décennie souhaites-tu voir ? ('b' pour revenir au menu principal)" )
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
                    if self.db_manager.execute_query(f'''SELECT * FROM {list_to_show[main_menu_choice - 1]} WHERE decade = {choices[choice_decade_int - 1][1]}'''):
                        self.show_remaining_list(choices[choice_decade_int - 1][1], list_to_show[main_menu_choice - 1])
                        # TODO : est ce que j'ai besoin de ce return ?
                        return choices[choice_decade_int - 1][1]
                    else:
                        print(f"Tous les albums ont été taggés pour les années {choices[choice_decade_int - 1][1]}.") 
                        print()
                        continue
                elif choice_decade_int in [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]:
                    if self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE decade = {choice_decade_int}'''):
                        self.show_remaining_list(choice_decade_int, list_to_show[main_menu_choice - 1])
                        # TODO : est ce que j'ai besoin de ce return ?
                        return choice_decade_int
                    else:
                        print(f"Tous les albums ont été taggés pour les années {choice_decade_int}.") 
                        print()
                        continue
                else:
                    print("Tu dois choisir une des options proposées.")
                    continue
            except:
                if choice_decade == "b":
                    self.main_menu()
                else:
                    print("Tu dois choisir une des options proposées.")
                    continue

    def show_remaining_list(self, choice, main_menu_choice):
        print()
        print(f"Voici la listes des albums pour les années {choice}.")
        print("""
n°   Artiste                        Album                          Annee
==== ============================== ============================== =====
""")
        rows = self.db_manager.execute_query(f'''SELECT * FROM {main_menu_choice} WHERE decade = {choice}''')
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
                self.show_remaining_list(decade, value=None)
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
                print(f"L'album a été ajouté à la liste des albums que tu aimes.")                
            else:
                print(f"L'album existe déjà dans la liste des albums que tu aimes.")
        else:
            print("L'album n'a pas été trouvé dans la liste des albums qu'il te reste à tagger.")
               
    def unliked_album(self, album_id):
        album = self.db_manager.execute_query(f"SELECT * FROM remaining_list WHERE album_id='{album_id}'")
        if album:
            if not self.db_manager.execute_query(f"SELECT * FROM unliked_list WHERE album_id='{album_id}'"):
                self.db_manager.execute_query('''INSERT INTO unliked_list VALUES (?,?,?,?,?)''', (album[0][0], album[0][1], album[0][2], album[0][3], album[0][4]))
                self.db_manager.execute_query('''DELETE FROM remaining_list WHERE album_id=?''', (album_id,))
                self.db_manager.connect().commit()
                print(f"L'album a été ajouté dans la liste des albums que tu n'aimes pas.")                
            else:
                print(f"L'album existe déjà dans la liste des albums que tu n'aimes pas.")
        else:
            print("L'album n'a pas été trouvé dans la liste des albums qu'il te reste à tagger.")

    def close(self):
        self.conn.close

class MainMenu:
    def __init__(self):
        self.introduction()
        self.connexion_menu()
         
    def introduction(self):
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
Elle contient actuellement 1084 albums.
    """)

    def connexion_menu(self):
        while True:
            print(" 1. se connecter")
            print(" 2. créer un nouveau profil")
            print(" 3. quitter")

            connexion_choice = input(">>> ")

            if connexion_choice == "1":                
                user_name = self.get_user_name() 
                print(f"Bonjour {user_name}, je me connecte à ta base de données...")
                User(user_name)
                break
            elif connexion_choice == "2":
                user_name = self.get_user_name() 
                print(f"Patiente un instant {user_name}, je prépare ta base de données...")
                User(user_name)
                break
            elif connexion_choice == "3":
                sys.exit()
            else:
                print("Tu dois choisir 1, 2 ou 3.")
                print()
                continue

    def get_user_name(self):
        print()
        print("Quel est ton pseudo ?")
        user_name = input(">>> ")
        print()
        return user_name


MainMenu()