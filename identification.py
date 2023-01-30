import itertools
import sqlite3
import os

PATH_DB = r"c:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\users.db"

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

class User:

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.mdp = ""

    def user_identification(self):
        with sqlite3.connect(PATH_DB) as connexion:
            curseur = connexion.cursor()
            # Vérification de la présence du pseudo dans la bdd
            curseur.execute(f'SELECT * FROM users WHERE pseudo="{self.pseudo}"')
            user_found = curseur.fetchall()                
            if user_found == []:
                print("Ton pseudo n'est pas dans la base.")
                self.create_new_user(curseur)
            else:
                for i in range(3):
                    print("Entre ton mot de passe :")
                    self.mdp = input(">>> ")
                    curseur.execute(f'SELECT * FROM users WHERE pseudo="{self.pseudo}"')
                    verify_mdp = curseur.fetchall()
                    if self.mdp == verify_mdp[0][2]:
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
        

    def create_new_user(self, curseur):
        print(f"Je crée un nouvel utilisateur dans ma base avec le pseudo : {self.pseudo}")
        curseur.execute(f"""INSERT INTO users (pseudo) VALUES ("{self.pseudo}");""")
        print("Entre ton mot de passe :")
        user_mdp = input(">>> ")
        curseur.execute(f"""UPDATE users SET mdp = ("{user_mdp}") WHERE pseudo = "{self.pseudo}";""")
        print("Ton compte a bien été créé.")
        # TODO : création de l'objet Playlist propre à l'utilisateur
        menu_access()


def get_user_identification():
    print("Entre ton pseudo :")
    pseudo = input(">>> ")
    user = User(pseudo)
    user.user_identification()

def menu_access():
    print("menu")


get_user_identification()








