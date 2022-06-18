from controllers.discord import token_login
from controllers.libs import *
from random import choice
import time

accounts = [x.split() for x in open("data/accounts.txt", 'r').readlines()]
channels = open("data/channels.txt", 'r').readlines()
wait_length = 10
periods = 10
messages = open("data/messages.txt", 'r').readlines()

for account in accounts:
    driver = Selenium.get_driver(proxy=account[2])
    driver, err = token_login(driver, account[1])
    for channel in channels:
        driver.get(channel)
        time.sleep(3)        
        for i in messages:
            driver.find_element(By.XPATH, ".//div[@role='textbox']").send_keys(i)
            driver.find_element(By.XPATH, ".//div[@role='textbox']").send_keys(Keys.ENTER)
            print("messaged channel")
        time.sleep(wait_length)
driver.close()