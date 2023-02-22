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

    def connect_db_user(self):
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
                self.decade_choice(int(main_menu_choice))
                print()
                print("Tape 'b' pour revenir au menu principal")
                while True:
                    back_to_menu = input(">>> ")
                    if back_to_menu == "b":
                        self.main_menu()
                    else:
                        print("Tu dois taper 'b' pour revenir au menu")                        
            elif main_menu_choice == "3":
                decade = self.decade_choice(int(main_menu_choice))
                # self.add_to_liked_or_unliked(decade)
                break
            elif main_menu_choice == "4":
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
                    if self.db_manager.execute_query(f'''SELECT * FROM albums WHERE decade = {choices[choice_decade_int - 1][1]}'''):
                        print("coucou 1 2 3")
                        # self.show_remaining_list(choices[choice_decade_int - 1][1], list_to_show[main_menu_choice - 1])
                    else:
                        print(f"Tous les albums ont été taggés pour les années {choices[choice_decade_int - 1][1]}.") 
                        print()
                        continue
                elif choice_decade_int in [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]:
                    if self.db_manager.execute_query(f'''SELECT * FROM remaining_list WHERE decade = {choice_decade_int}'''):
                        print("coucou 19..")
                        # self.show_remaining_list(choice_decade_int, list_to_show[main_menu_choice - 1])
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
                User(username).connect_db_user()
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
