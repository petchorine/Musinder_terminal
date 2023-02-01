import sqlite3
import os

PATH_DB = r"c:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\users.db"
def users_database_creation():
    if os.path.exists(PATH_DB):
        pass
    else:
        with sqlite3.connect(PATH_DB) as connexion:
            curseur = connexion.cursor()
            curseur.execute("""CREATE TABLE users (
                user_id INTEGER NOT NULL PRIMARY KEY,
                pseudo VARCHAR,
                mdp VARCHAR);""")      
users_database_creation()

class DatabaseManager:
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db

    def connect(self):
        return sqlite3.connect(self.path_to_db)

    def execute_query(self, query):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()

class User:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.mdp = ""
        self.db_manager = DatabaseManager(PATH_DB)

    def user_identification(self):
        # Vérification de la présence du pseudo dans la bdd
        result = self.db_manager.execute_query(f'SELECT * FROM users WHERE pseudo="{self.pseudo}"')
        user_found = result
        if user_found == []:
            print("Ton pseudo n'est pas dans la base.")
            self.create_new_user()
        else:
            for i in range(3):
                print("Entre ton mot de passe :")
                self.mdp = input(">>> ")
                result = self.db_manager.execute_query(f'SELECT * FROM users WHERE pseudo="{self.pseudo}"')
                verify_mdp = result[0][2]
                if self.mdp == verify_mdp:
                    print("pseudo + mdp = ok")                                        
                    menu_access()
                    break
                else:
                    if i < 2:
                        print("Le mot de passe ne correspond pas au pseudo")
                    else:
                        print()
                        print("Désolé, retape ton pseudo")
                        get_user_identification()
                        break

    def create_new_user(self):
        print(f"Je crée un nouvel utilisateur dans ma base avec le pseudo : {self.pseudo}")
        self.db_manager.execute_query(f"""INSERT INTO users (pseudo) VALUES ("{self.pseudo}");""")
        print("Entre ton mot de passe :")
        user_mdp = input(">>> ")
        self.db_manager.execute_query(f"""UPDATE users SET mdp = ("{user_mdp}") WHERE pseudo = "{self.pseudo}";""")
        print("Ton compte a bien été créé.")
        menu_access()


def menu_access():
    print("menu")


def get_user_identification():
    print("Entre ton pseudo :")
    pseudo = input(">>> ")
    user = User(pseudo)
    user.user_identification()

get_user_identification()