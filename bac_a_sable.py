import itertools
import sqlite3
import os


def users_database_creation():
    if os.path.exists(r"c:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\users.db"):
            pass
    else:
        connexion = sqlite3.connect(r"c:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\users.db")
        curseur = connexion.cursor()
        curseur.execute("""CREATE TABLE users (
            user_id INTEGER NOT NULL PRIMARY KEY,
            pseudo VARCHAR,
            mdp VARCHAR);""")
        connexion.commit()
        connexion.close()

class User:

    connexion = sqlite3.connect(r"c:\Users\chris\Desktop\monPyhon\mes_projets_python\musinder\V0\users.db")
    curseur = connexion.cursor()
    id_iter = itertools.count()

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.mdp = ""
        self.id = next(self.id_iter)

    def user_identification(self):

        # Vérification de la présence du pseudo dans la bdd
        self.curseur.execute(f'SELECT * FROM users WHERE pseudo="{self.pseudo}"')
        user_found = self.curseur.fetchall()                
        if user_found == []:
            print("Ton pseudo n'est pas dans la base.")
            self.create_new_user()
        else:
            print("Entre ton mot de passe :")
            self.mdp = input(">>> ")
            self.curseur.execute(f'SELECT * FROM users WHERE pseudo="{self.pseudo}"')
            verify_mdp = self.curseur.fetchall()
            if self.mdp == verify_mdp[0][2]:
                print("pseudo + mdp = ok")
            else:
                print("Le mot de passe ne correspond pas au pseudo")
        
        self.connexion.commit()
        self.connexion.close()

    def create_new_user(self):
        print(f"Je crée un nouvel utilisateur dans ma base avec le pseudo : {self.pseudo}")
        self.curseur.execute(f"""INSERT INTO users (pseudo) VALUES ("{self.pseudo}");""")
        print("Entre ton mot de passe :")
        user_mdp = input(">>> ")
        self.curseur.execute(f"""UPDATE users SET mdp = ("{user_mdp}") WHERE pseudo = "{self.pseudo}";""")
        print("Ton compte a bien été créé.")


def get_user_identification():
    print("Entre ton pseudo :")
    pseudo = input(">>> ")
    user = User(pseudo)
    user.user_identification()

users_database_creation()
get_user_identification()









