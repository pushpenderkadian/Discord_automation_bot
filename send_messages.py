from controllers.discord import *
import os

if __name__ == '__main__':
    
    accounts = [x.split() for x in open("data/accounts.txt", 'r').readlines()]
    messages = get_messages()
    filter_option = input("E for Exclusive filter\nI for Inclusive filter\n>")
    method_option = int(input("Select messaging method:\n1: Logging and messaging(You need the users logged)\n2: DM on the fly (slower, but assured to have access to all visible members)\n>"))
    total_dm = 0
    if method_option == 1:
        target_list = [x.replace(' ', '_') for x in input("Enter the servers you wish to target, separated by commas.\nLeave blank to target all servers\n>").split(',')]
        target = {}
        for username_list in os.listdir("target/"):
            if username_list[:-4] in target_list or target_list == ['']:
                target[username_list[:-4]] = pickle.load(open("target/"+username_list, 'rb'))
        for account in accounts:
            no_dms = send_messages(proxy=account[2],email=account[0],password=account[1],target=target,messages=messages, f_option=filter_option)
            print(f"Number of DMs sent: {no_dms}")
            total_dm += no_dms
            print(f"Total DMs until now: {total_dm}")
    elif method_option == 2:
        for account in accounts:
            no_dms = send_messages_oldver(account[2], account[0], account[1], filter_option, messages)
            print(f"Number of DMs sent: {no_dms}")
            total_dm += no_dms
            print(f"Total DMs until now: {total_dm}")
    else:
        print("Invalid option!")
        exit()