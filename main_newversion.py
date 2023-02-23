import sqlite3
import requests
from bs4 import BeautifulSoup
import os
import sys

class DatabaseManager:
    def __init__(self):
        self.path_to_db = r'C:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\musinder.db'
      
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

class AlbumDB:
    def __init__(self):
        self.url_wiki = r"https://fr.wikipedia.org/wiki/Les_1001_albums_qu%27il_faut_avoir_%C3%A9cout%C3%A9s_dans_sa_vie"
        self.db_manager = DatabaseManager()

        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS albums (album_id integer primary key autoincrement, numero_album text, artist text, title text, year text, decade integer)''')
        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS users (user_id integer primary key autoincrement, username text)''')
        self.db_manager.execute_query('''CREATE TABLE IF NOT EXISTS albums_rating (album_id text, user_id integer, rating text not null, primary key (album_id, user_id), foreign key (album_id) references albums (album_id), foreign key (user_id) references users (user_id))''')
               
        self.add_albums_to_db()
        self.db_manager.connect().commit()

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
                    new_entry = {"numero_album": index_id, "artist": artist, "title": title, "year": year, "decade": decade}
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
                insert_query = "INSERT INTO albums (numero_album, artist, title, year, decade) VALUES (?,?,?,?,?)"
                self.db_manager.execute_query(insert_query, (album["numero_album"], album["artist"], album["title"], album["year"], album["decade"]))
                self.db_manager.connect().commit()


if not os.path.exists(fr'C:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\musinder.db'):
    AlbumDB()

class User:
    def __init__(self, username):
        self.username = username
        self.db_manager = DatabaseManager()

        self.db_manager.connect().commit()

    def add_user_to_db(self):
        query = "SELECT 1 FROM users WHERE username=?"
        result = self.db_manager.execute_query(query, (self.username,))
        
        if result:
            print("Ce pseudo existe déjà dans ma base de données.")
            pass
        else:
            print(f"Patiente un instant {self.username}, je prépare ta base de données...")
            self.db_manager.execute_query("INSERT INTO users (username) VALUES (?)", (self.username,))
            self.db_manager.connect().commit()

    def connect_user_to_db(self):
        query = "SELECT 1 FROM users WHERE username=?"
        result = self.db_manager.execute_query(query, (self.username,))
        
        if result:
            self.main_menu()
        else:
            print("Ce pseudo n'est pas dans ma base de données.")

    def main_menu(self):
        print()
        print(f"Bonjour {self.username}, que veux-tu faire ?")
        print(" 1. voir la liste par décennie des albums que j'ai aimé")
        print(" 2. voir la liste par décennie des albums que je n'ai pas aimé")
        print(" 3. voir la liste par décennie des albums qu'il te reste à tagger")
        print(" 4. quitter")
    
        while True:
            main_menu_choice = input(">>> ")
            
            if main_menu_choice == "1" or main_menu_choice == "2":
                self.get_list_to_show(int(main_menu_choice))
                print()
                print("Tape 'b' pour revenir au menu principal")
                while True:
                    back_to_menu = input(">>> ")
                    if back_to_menu == "b":
                        self.main_menu()
                    else:
                        print("Tu dois taper 'b' pour revenir au menu")
            elif main_menu_choice == "3":
                decade = self.get_list_to_show(int(main_menu_choice))
                self.menu_before_tagging(decade)
                break
            elif main_menu_choice == "4":
                sys.exit()
            else:
                print("Tu dois choisir entre 1, 2, 3 ou 4")
                continue     
    
    def get_decade(self):
        decades_list = [(1, 1950), (2, 1960), (3, 1970), (4, 1980), (5, 1990), (6, 2000), (7, 2010), (8, 2020)]
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
            
            if choice_decade in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                choice_decade = decades_list[(int(choice_decade) - 1)][1]
                break
            elif choice_decade in ["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"]:
                choice_decade = int(choice_decade)
                break
            elif choice_decade == "b":
                self.main_menu()
            else:
                print("Ton choix n'est pas dans la liste.")
                continue
    
        return choice_decade

    def get_list_to_show(self, main_menu_choice):
        decade = self.get_decade()
        user = self.db_manager.execute_query(f'''select user_id from users where username = "{self.username}";''')[0][0]
        if main_menu_choice == 1:
            rows = self.db_manager.execute_query(f'''  
                select a.album_id, a.artist, a.title, a.year
                from albums_rating as r, users as u, albums as a
                WHERE decade = {decade}
                and r.user_id = {user}
                and r.rating = "liked"
                and r.user_id = u.user_id
                and r.album_id = a.album_id;''')
        elif main_menu_choice == 2:
            rows = self.db_manager.execute_query(f'''  
                select a.album_id, a.artist, a.title, a.year
                from albums_rating as r, users as u, albums as a
                WHERE decade = {decade}
                and r.user_id = {user}
                and r.rating = "unliked"
                and r.user_id = u.user_id
                and r.album_id = a.album_id;''')
        else:
            rows = self.db_manager.execute_query(f'''
                SELECT a.album_id, a.artist, a.title, a.year
                FROM albums as a
                WHERE decade = {decade}  
                AND a.album_id NOT IN (
                    SELECT album_id FROM albums_rating
                    WHERE user_id = (SELECT user_id FROM users WHERE username = "{self.username}"));''')
        self.show_list(decade, rows)
        return decade    

    def show_list(self, decade, rows):
            print()
            print(f"Voici la listes des albums pour les années {decade}.")
            print("""
n°   Artiste                        Album                          Annee
==== ============================== ============================== =====
""")

            for row in rows:
                print(str(row[0]).ljust(4), row[1][:30].ljust(30, "."), 
                        row[2][:27].ljust(30, "."), row[3].rjust(4))

    def menu_before_tagging(self, decade):
        while self.db_manager.execute_query(f'''SELECT 1
                                                FROM albums as a
                                                WHERE decade = {decade} 
                                                AND a.album_id NOT IN (
                                                    SELECT album_id FROM albums_rating
                                                    WHERE user_id = (SELECT user_id FROM users WHERE username = '{self.username}')
                                                );'''):
            print()
            print("Que souhaites-tu faire ?")
            print(" 1. tagger un nouvel album")
            print(f" 2. afficher à nouveau la liste des albums des années {decade}")
            print(" 3. revenir au menu et changer de décennie")
            user_choice = input(">>> ")

            if user_choice == "1":
                self.add_to_liked_or_unliked(decade)
            elif user_choice == "2":
                rows = self.db_manager.execute_query(f'''
                SELECT a.album_id, a.artist, a.title, a.year
                FROM albums as a
                WHERE decade = {decade}  
                AND a.album_id NOT IN (
                    SELECT album_id FROM albums_rating
                    WHERE user_id = (SELECT user_id FROM users WHERE username = "{self.username}"));''')
                self.show_list(decade, rows)
            elif user_choice == "3":
                self.main_menu()
            else:
                print("Tu dois choisir entre 1, 2 ou 3.")
                continue        
        
        # TODO : ajouter sortie quand le while est False : tous les albums de cette décennie ont été taggés

    def add_to_liked_or_unliked(self, decade):
        # TODO : comment empecher de choisir un album qui est déjà taggé
        
        while True:
            print()
            print("Tape le n° de l'album :")
            album_choice = input(">>> ")
            if album_choice.isdecimal():
                album = self.db_manager.execute_query(f'''SELECT a.title, a.artist 
                                                        FROM albums as a
                                                        WHERE decade = {decade}
                                                        AND a.album_id = {album_choice}''')
                if album:
                    print()
                    print(f"As-tu aimé l'album '{album[0][0]}' de {album[0][1]} ?")
                    print(" 1. oui")
                    print(" 2. non")
                    user_choice = input(">>> ")

                    if user_choice == "1":
                        print("aimé")
                        self.db_manager.execute_query(f'''INSERT INTO albums_rating (album_id, user_id, rating)
                        VALUES ({album_choice}, (SELECT user_id FROM users WHERE username = '{self.username}'), 'liked');''')
                        continue
                    elif user_choice == "2":
                        print("pas aimé")
                        self.db_manager.execute_query(f'''INSERT INTO albums_rating (album_id, user_id, rating)
                        VALUES ({album_choice}, (SELECT user_id FROM users WHERE username = '{self.username}'), 'unliked');''')
                        continue
                    else:
                        print("Tu dois choisir 1 ou 2.")
                        self.menu_before_tagging()
                else:
                    print("Cet album n'est pas dans la liste.")
                    continue
            else:
                print("Tu dois taper le n° de l'album.")
                continue



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
                username = self.get_username() 
                User(username).connect_user_to_db()
                break
            elif connexion_choice == "2":
                username = self.get_username() 
                User(username).add_user_to_db()
                break
            elif connexion_choice == "3":
                sys.exit()
            else:
                print("Tu dois choisir 1, 2 ou 3.")
                print()
                continue

    def get_username(self):
        print()
        print("Quel est ton pseudo ?")
        username = input(">>> ")
        print()
        return username


MainMenu()
