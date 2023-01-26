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

    id_iter = itertools.count()
    def __init__(self, pseudo, mdp):
        self.pseudo = pseudo
        self.mdp = mdp
        self.id = next(self.id_iter)

    def identif(self):
        connexion = sqlite3.connect("users.db")
        curseur = connexion.cursor()

        # Vérification de la présence du pseudo dans la bdd
        curseur.execute(f'SELECT * FROM users')
        # curseur.execute(f'SELECT * FROM users WHERE pseudo="{self.pseudo}"')
        user_found = curseur.fetchall()
        print(user_found)
        
        if user_found == []:
            print("Ton pseudo n'est pas dans la base.")
            # create_new_user(curseur, user_pseudo)
        else:
            print("Ton pseudo est dans la base.")
            # print("Quel est ton mot de passe ?")


def identification_user(connexion):
    curseur = connexion.cursor()
    print("Entre ton pseudo :")
    user_pseudo = input(">>> ")

    # Vérification de la présence du pseudo dans la bdd
    curseur.execute(f'SELECT * FROM users WHERE pseudo="{user_pseudo}"')
    user_found = curseur.fetchall()

    if user_found == []:
        print("Ton pseudo n'est pas dans la base.")
        create_new_user(curseur, user_pseudo)
    else:
        print("Ton pseudo est dans la base.")
        print("Quel est ton mot de passe ?")
        user_mdp = input(">>> ")
        curseur.execute(f'SELECT * FROM users WHERE pseudo="{user_pseudo}"')
        mdp_ok = curseur.fetchall()
        if user_mdp == mdp_ok[0][2]:
            print("pseudo + mdp = ok")
        else:
            print("Le mot de passe ne correspond pas au pseudo")

def create_new_user(curseur, user_pseudo):
        print(f"Je crée un nouvel utilisateur dans ma base avec le pseudo : {user_pseudo}")
        curseur.execute(f"""INSERT INTO users (pseudo) VALUES ("{user_pseudo}");""")
        print("Entre ton mot de passe :")
        user_mdp = input(">>> ")
        curseur.execute(f"""UPDATE users SET mdp = ("{user_mdp}") WHERE pseudo = "{user_pseudo}";""")
        print("Ton compte a bien été créé.")



def test():
    pseudo = "toto"
    mdp = "123"
    user = User(pseudo, mdp)

    user.identif()

users_database_creation()
test()


# connexion = sqlite3.connect("users.db")


# identification_user(connexion)

# connexion.commit()
# connexion.close()










