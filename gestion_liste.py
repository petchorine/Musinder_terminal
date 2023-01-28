import copy

all_dico = {"21": "a", "22": "b", "23": "c", "24": "d", "25": "e", "26": "f"}

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
        liked.append()
        # del remaining_list
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
        for k, v in remaining_list.items():
            print(f"{k}. {v}")
        print()
        add_to_liked_or_unliked()
    else:
        print("menu")


intro()


print()
print("****************************************************************")
print("all_dico       : ", len(all_dico), " - ", all_dico)
print("remaining_list : ", len(remaining_list), " - ", remaining_list )
print("liked          : ", len(liked), " - ", liked)
print("unliked        : ", len(unliked), " - ", unliked )