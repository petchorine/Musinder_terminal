import copy

all_dico = [{'numero': '1', 'artiste': 'Frank Sinatra', 'titre': 'In the Wee Small Hours', 'annee': '1955'}, {'numero': '2', 'artiste': 'Elvis Presley', 'titre': 'Elvis Presley (album)', 'annee': '1956'}, {'numero': '3', 'artiste': 'The Louvin Brothers', 'titre': 'Tragic Songs of Life', 'annee': '1956'}]


remaining_list = copy.copy(all_dico)
liked = []
unliked = []


def add_to_liked_or_unliked():
    while remaining_list:
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
            
            for album_present_or_not in remaining_list:
                if album_choice in album_present_or_not.values():
                    print()
                    print("As-tu aimé cet album ?")
                    print(" 1. oui")
                    print(" 2. non")
                    user_choice = input(">>> ")

                    if user_choice == "1":       
                        for album in remaining_list:
                            if album["numero"] == album_choice:
                                liked.append(album)
                                remaining_list.remove(album)
                                break
                    elif user_choice == "2":
                        for album in remaining_list:
                            if album["numero"] == album_choice:
                                unliked.append(album)
                                remaining_list.remove(album)
                                break
                    else:
                        print("Tu dois choisir 1 ou 2.")
                        add_to_liked_or_unliked()
                else:
                    print("Cet album n'est pas dans la liste.")
                    break
        elif user_choice == "2":
            show_remaining_list()
        elif user_choice == "3":
            print("menu")
            return remaining_list, liked, unliked
        else:
            print("Tu dois choisir entre 1, 2 ou 3.")
            continue

    print("Tous les albums ont été taggés.")   

def show_remaining_list():
        print()
        print("""
n°   Artiste                        Album                          Annee
==== ============================== ============================== =====
""")
        for toto in remaining_list:
            print(toto["numero"].ljust(4), toto["artiste"][:30].ljust(30, "."), 
                    toto["titre"][:27].ljust(30, "."), toto["annee"].rjust(4))

def intro():
    # TODO : menu choix quelle décénie
    print()
    print("Voici les albums qu'il te reste à tagger :")
    show_remaining_list()
    add_to_liked_or_unliked()

intro()


print()
print("****************************************************************")
print("all_dico       : ", len(all_dico))
print("remaining_list : ", len(remaining_list), " - ", remaining_list )
print("liked          : ", len(liked) , " - ", liked)
print("unliked        : ", len(unliked), " - ", unliked )