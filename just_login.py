import selenium
from controllers.discord import *

if __name__ == '__main__':
    account = open("data/accounts.txt", "r").readlines()[0].split()
    driver = Selenium.get_driver(proxy=account[2])
    driver, own_username = token_login(driver,account[1])
    input("Press ENTER to quit.")
    driver.close()
    exit()