from controllers.discord import token_login
from controllers.libs import *

accounts = [x.split() for x in open("data/accounts.txt", 'r').readlines()]
invites = open("data/invites.txt", 'r').readlines()

for account in accounts:
    driver = Selenium.get_driver(proxy=account[2])
    driver, own_username = token_login(driver,account[1])

    for invite in invites:
        driver.get(invite)
        driver.implicitly_wait(5)
        driver.find_element(By.TAG_NAME, "button").click()
        driver.implicitly_wait(5)
        try:
            driver.find_element(By.TAG_NAME, "button").click()
            driver.implicitly_wait(5)
        except:
            pass

    driver.close()
