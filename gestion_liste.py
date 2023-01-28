import copy

all_dico = [{'numero': '1', 'artiste': 'Frank Sinatra', 'titre': 'In the Wee Small Hours', 'annee': '1955'}, {'numero': '2', 'artiste': 'Elvis Presley', 'titre': 'Elvis Presley (album)', 'annee': '1956'}, {'numero': '3', 'artiste': 'The Louvin Brothers', 'titre': 'Tragic Songs of Life', 'annee': '1956'}, {'numero': '4', 'artiste': 'Louis Prima', 'titre': 'The Wildest!', 'annee': '1956'}, {'numero': '5', 'artiste': 'Fats Domino', 'titre': 'This is Fats', 'annee': '1956'}]


remaining_list = copy.copy(all_dico)
liked = []
unliked = []


def add_to_liked_or_unliked():
    print("Tape le n° de l'album :")
    album_choice = input(">>> ")
    print()
    print("As-tu aimé cet album ?")
    print(" 1. oui")
    print(" 2. non")
    user_choice = input(">>> ")

    if user_choice == "1":       
        for album in remaining_list:
            if album["numero"] == album_choice:
                liked.append(album_choice)
                remaining_list.remove(album)
                break

    elif user_choice == "2":
        unliked.append()
        # del remaining_list
    
    while True:
        print("Veux-tu tagger un nouvel album ?")
        print(" 1. oui")
        print(" 2. non")
        user_choice = input(">>> ")

        if user_choice == "1":
            add_to_liked_or_unliked()
        elif user_choice == "2":
            break
        else:
            print("Tu dois choisir 1 ou 2.")


def intro():
    print("Que souhaites-tu faire ?")
    print(" 1. tagger un nouvel album")
    print(" 2. revenir au menu")
    user_choice = input(">>> ")

    if user_choice == "1":
        print()
        print("Titre")
        
        # TODO : afficher le dictionnaire

        # add_to_liked_or_unliked()
    else:
        print("menu")


intro()


print()
print("****************************************************************")
print("all_dico       : ", len(all_dico), " - ", all_dico)
print("remaining_list : ", len(remaining_list), " - ", remaining_list )
print("liked          : ", len(liked), " - ", liked)
print("unliked        : ", len(unliked), " - ", unliked )