import pickle


skip = pickle.load(open("data/skip.pkl","rb"))
while True:
    option = input("\nA to add a new name to skip\nC to clear skip\nS to show the contents of skip\nQ to quit\n>")
    if option == 'A':
        print("Q to quit.")
        while True:
            name = input("Name: ")
            if name == 'Q':
                break
            else:
                skip.append(name)
    elif option == 'C':
        print("Cleared!")
        skip = []
    elif option == 'S':
        for name in skip:
            print("\t"+name)
    elif option == 'Q':
        pickle.dump(skip, open("data/skip.pkl", "wb"))
        break