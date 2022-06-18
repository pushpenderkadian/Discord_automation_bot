import pickle
import os

print("Welcome to the filter manager!")
exclusive = pickle.load(open("data/exclusive_filter.pkl", "rb"))
inclusive = pickle.load(open("data/inclusive_filter.pkl", "rb"))

while True:
    option = input("S to show filters\nA to add to a filter\nD to delete a particular entry\nC to clear a filter\nQ to quit\n>")

    if option == "S":
        print("Exclusive filter:")
        print("\t"+"\n\t".join(exclusive))
        print("Inclusive filter:")
        print("\t"+"\n\t".join(inclusive))
    elif option == "A":
        foption = input("Add to which filter?\nE for exclusive\nI for inclusive\n>")
        print("Please, select a server that contains the desired role:")
        servers = {}
        for n, server in enumerate(os.listdir("target/")):
            print(f"\t{n}: {server}")
            servers[n] = "target/"+server
        option = int(input(">"))

        server = pickle.load(open(servers[option], "rb"))
        roles = []
        for person in server:
            if person == 'server':
                continue
            roles = list(set.union(set(server[person]), set(roles)))

        while True:
            print("Roles:")
            for n, role in enumerate(roles):
                print(f"\t{n}: {role}")
            print("\tQ to quit")
            print("Please select a role number")
            option = input(">")
            if option == "Q":
                break
            else:
                option = int(option)

            selected_role = roles[option]
            
            if foption == "E":
                exclusive.append(selected_role)
            elif foption == "I":
                inclusive.append(selected_role)
    elif option == "D":
        foption = input("Delete from which filter?\nE for exclusive\nI for inclusive\n>")
        if foption == "E":
            print("Exclusive filter:")
            for n, role in enumerate(exclusive):
                print(f"\t{n} : {role}")
        elif foption == "I":
            print("Inclusive filter:")
            for n, role in enumerate(inclusive):
                print(f"\t{n} : {role}")
        print("\tC to cancel")
        option = input(">")
        if option == 'C':
            continue
        else:
            if foption == "E":
                exclusive.pop(int(option))
            elif foption == "I":
                inclusive.pop(int(option))
    elif option == 'C':
        foption = input("Clear which filter?\nE for exclusive\nI for inclusive\n>")
        if foption == "E":
            exclusive = []
        elif foption == "I":
            inclusive = []
    elif option == "Q":
        pickle.dump(exclusive, open("data/exclusive_filter.pkl", "wb"))
        pickle.dump(inclusive, open("data/inclusive_filter.pkl", "wb"))
        exit()