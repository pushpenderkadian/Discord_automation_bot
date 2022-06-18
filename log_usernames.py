from controllers.discord import *

if __name__ == '__main__':
    account = open("data/accounts.txt", "r").readlines()[0].split()
    log_usernames(proxy=account[2],email=account[0],password=account[1])
