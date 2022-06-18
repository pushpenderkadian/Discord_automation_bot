from controllers.libs import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pickle

t = pickle.load(open('controllers/time.pkl', 'rb')) #adjust to your liking

def check_ban(driver, id):
    try:
        driver.find_element(By.XPATH, ".//div[@class='title-wZCcDo marginTop20-3TxNs6']")
        accounts = list(open("data/accounts.txt", "r"))
        for n, account in enumerate(accounts):
            if id in account:
                accounts.pop(n)
        with open("data/accounts.txt", "w") as f:
            f.write("\n".join(accounts))
        return True
    except:
        return False
#token login
def token_login(driver, token):
    login_link = 'https://discord.com/app'
    driver.get(login_link)
    sc = """
    function login(token) {
        setInterval(() => {
        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
        }, 50);
        setTimeout(() => {
        location.reload();
        }, 2500);
    }

    login(arguments[0]);
    """
    driver.execute_script(sc, token)
    time.sleep(t)
    driver.refresh()
    while True:
        if check_ban(driver, token):
            print("Account banned! removed from list.")
            return 0,0
        try:
            time.sleep(5)
            own_username = driver.find_element(By.XPATH, ".//div[@class='size14-e6ZScH title-eS5yk3']").get_attribute("innerHTML")
            break
        except:
            print("Waiting for the page to load...")
            time.sleep(2*t)

    return driver, own_username

def log_usernames(proxy=None,email=None,password=None):

    if proxy == "NONE":
        proxy = None
    target_all = input("Target all servers? (Y/N)") == "Y"
    driver = Selenium.get_driver(proxy)
    driver, own_username = token_login(driver,password)
    if driver == own_username == 0:
        return {}

    skip = []
    print('Logged into ', email)
    actions = ActionChains(driver)

    servers = WebDriverWait(driver, 3*t).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Servers']/div")))
    for server_no in range(len(servers)):

        server = servers[server_no]
        server_name = server.find_element(By.CSS_SELECTOR, 'foreignObject > div').get_attribute('aria-label').strip()
        if not target_all:
            if input(f"Log server {server_name}? (Y/N)") == 'N':
                continue
        print(f"Starting to log members from server {server_name}")
        actions.move_to_element(server).perform()
        driver.execute_script("arguments[0].scrollBy(40, 0)", driver.find_element(By.XPATH, ".//div[@class='scroller-1Bvpku none-2Eo-qx scrollerBase-289Jih']"))

        server.click()
        server_name = " ".join(server_name.split()[2:]) if "mentions" in server_name.lower() else server_name
        log = {"server": server_name}
        driver.implicitly_wait(t)
            
        driver.execute_script("arguments[0].scrollTo(0,0)", driver.find_element(By.XPATH, "//div[@class='members-1998pB thin-1ybCId scrollerBase-289Jih fade-2kXiP2']"))
        scroll_height = int(driver.find_element(By.XPATH, "//div[@class='members-1998pB thin-1ybCId scrollerBase-289Jih fade-2kXiP2']").get_attribute("scrollHeight"))

        for scroll in range(0,scroll_height,100):
            driver.execute_script("arguments[0].scrollTo(0,arguments[1])", driver.find_element(By.XPATH, "//div[@class='members-1998pB thin-1ybCId scrollerBase-289Jih fade-2kXiP2']"), scroll)

            time.sleep(t/3)

            visible = driver.find_elements(By.XPATH, ".//div[@aria-label='Members']/div//div[contains(@class, 'name')]/span")
            for person in visible:
                try:
                    if check_ban(driver, email):
                        return log
                    name = person.get_attribute('innerHTML')
                    if name in skip:
                        continue
                    elif name == own_username:
                        print("Skipping self.")
                        continue
                    elif len(person.find_elements(By.XPATH, "../../span[contains(@class,'botTag')]")) > 0:
                        print(f"Skipping bot {name}")
                        skip.append(name)
                        continue
                    else:
                        person.click()
                        driver.implicitly_wait(t)
                        
                        tags = [x.get_attribute('aria-label') for x in driver.find_elements(By.XPATH, ".//div[@aria-label='Roles' or @aria-label='Role']/div")]
                        print(f'Tags: {tags}')
                        username = "".join([x.get_attribute('innerHTML') for x in driver.find_elements(By.XPATH, ".//div[@class='headerTagNoNickname-3qrd77 headerTag-3GFl76 nameTag-m8r81H' or @class='headerTagWithNickname-3l_x6x headerTag-3GFl76 nameTag-m8r81H']/span")])
                        log[username] = tags
                        print(f"Logging {name}\nTags: {tags}")

                        driver.find_element(By.XPATH, ".//div[@role='dialog']").send_keys(Keys.ESCAPE)
                        skip.append(name)
                except Exception as e:
                    if type(e) != NoSuchElementException and type(e) != StaleElementReferenceException:
                        print(e)
                    else:
                        break
                pickle.dump(log, open(f"target/{server_name.replace(' ', '_')}.pkl", "wb"))
        servers = WebDriverWait(driver, 3*t).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Servers']/div")))
    print("Succesfully logged usernames!")

    return log

def send_messages(email, password, proxy, target, messages, f_option):

    if f_option == "E":
        exclude = pickle.load(open("data/exclusive_filter.pkl", "rb"))
    else:
        include_f = pickle.load(open("data/inclusive_filter.pkl", "rb"))

    if proxy == "NONE":
        proxy = None

    messaged = []
    driver = Selenium.get_driver(proxy)
    driver, own_username = token_login(driver,password)

    if driver == own_username == 0:
        return 0

    for server, people in target.items():
        
        for person, tags in people.items():
            if check_ban(driver, email):
                return len(messaged)
            if f_option == 'E':
                intersection = set.intersection(set(exclude), set(tags))
                if len(intersection) > 0:
                    print(f"Skipping {person}\n    Tags: {','.join(intersection)}")
                    continue
            else:
                intersection = set.intersection(set(include_f), set(tags))
                if  len(intersection) > 0:
                    print(f"Skipping {person}\n    Tags: {','.join(intersection)}")
                    continue

            driver.find_element(By.XPATH, ".//button[@class='searchBarComponent-32dTOx']").click()
            driver.implicitly_wait(t)
            driver.find_element(By.XPATH, ".//input[@class='input-2VB9rf']").send_keys(person)
            driver.implicitly_wait(t)
            if len(driver.find_elements(By.XPATH, ".//div[@class='emptyState-2gL-9T']")) > 0:
                print(person, 'not found.')
                driver.find_element(By.XPATH, ".//input[@class='input-2VB9rf']").send_keys(Keys.ESCAPE*2)
                continue
            driver.find_element(By.XPATH, ".//input[@class='input-2VB9rf']").send_keys(Keys.ENTER)
            time.sleep(t)
            
            print(own_username,'is DMing',person)
            msgbox = driver.find_element(By.XPATH, ".//div[@role='textbox']")

            for m in messages:
                msgbox.send_keys(m+"\n")
                time.sleep(t/10)

            messaged.append(person)

    return len(messaged)

def send_messages_oldver(proxy=None,email=None,password=None,f_option='E',messages=None):

    target_all = input("Target all servers? (Y/N)") == "Y"
    if f_option == "E":
        exclude = pickle.load(open("data/exclusive_filter.pkl", "rb"))
    else:
        include_f = pickle.load(open("data/inclusive_filter.pkl", "rb"))

    if proxy == "NONE":
        proxy = None

    driver = Selenium.get_driver(proxy)
    driver, own_username = token_login(driver,password)

    if driver == own_username == 0:
        return 0

    #servers rotates
    messaged = []
    no_of_dms = 0
    skip = pickle.load(open('data/skip.pkl', 'rb'))
    print('-----Bot Using Email :: ', email)
    actions = ActionChains(driver)
    servers = WebDriverWait(driver, 3*t).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Servers']/div")))
    for server_no in range(len(servers)):
        server = servers[server_no]
        server_name = server.find_element(By.CSS_SELECTOR, 'foreignObject > div').get_attribute('aria-label').strip()
        server_name = " ".join(server_name.split()[2:]) if "mentions" in server_name.lower() else server_name
        if not target_all:
            if input(f"Target server {server_name}? (Y/N)") == 'N':
                continue
        actions.move_to_element(server).perform()
        driver.execute_script("arguments[0].scrollBy(40, 0)", driver.find_element(By.XPATH, ".//div[@class='scroller-1Bvpku none-2Eo-qx scrollerBase-289Jih']"))

        print(f"Starting to message server {server_name}")
        server.click()
            
        driver.implicitly_wait(t)
            
        driver.execute_script("arguments[0].scrollTo(0,0)", driver.find_element(By.XPATH, "//div[@class='members-1998pB thin-1ybCId scrollerBase-289Jih fade-2kXiP2']"))
        scroll_height = int(driver.find_element(By.XPATH, "//div[@class='members-1998pB thin-1ybCId scrollerBase-289Jih fade-2kXiP2']").get_attribute("scrollHeight"))

        for scroll in range(0,scroll_height,200):
            if check_ban(driver, email):
                return no_of_dms
            driver.execute_script("arguments[0].scrollTo(0,arguments[1])", driver.find_element(By.XPATH, "//div[@class='members-1998pB thin-1ybCId scrollerBase-289Jih fade-2kXiP2']"), scroll)

            time.sleep(t/3)

            visible = driver.find_elements(By.XPATH, ".//div[@aria-label='Members']/div")
            #driver.find_elements(By.XPATH, f".//div[contains(@class, 'member')]")
            for person in visible:
                pickle.dump(skip, open('data/skip.pkl' , 'wb'))
                try:
                    name = person.find_element(By.XPATH, ".//div[contains(@class, 'name')]/span").get_attribute('innerHTML')
                    if name in skip:
                        continue
                    if name == own_username:
                        #print("Skipping self.")
                        continue
                    if len(person.find_elements(By.XPATH, ".//span[contains(@class,'botTag')]")) > 0:
                        print(f"Skipping bot {name}")
                        skip.append(name)
                        continue

                    #time.sleep(random.randint(1, 3))
                    person.find_element(By.XPATH, ".//div[contains(@class, 'avatar')]").click()
                    driver.implicitly_wait(t/2)
                    
                    try:
                        ele = driver.find_element(By.XPATH,'//div[@aria-label="Close"]')
                        ele.click()
                        time.sleep(t/3)
                        person.click()
                    except:
                        pass
                
                    tags = [x.get_attribute('aria-label') for x in driver.find_elements(By.XPATH, ".//div[@aria-label='Roles' or @aria-label='Role']/div")]
                       
                    if f_option == 'E':
                        intersection = set.intersection(set(exclude), set(tags))
                        if len(intersection) > 0:
                            print(f"Skipping {name}\n    Tags: {','.join(intersection)}")
                            skip.append(name)
                            continue
                    else:
                        intersection = set.intersection(set(include_f), set(tags))
                        if len(intersection) > 0:
                            print(f"Skipping {name}\n    Tags: {','.join(intersection)}")
                            skip.append(name)
                            continue

                    message_element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//div[@class='inputWrapper-31_8H8']/input")))
                    print(own_username,' is DM-ing ' + name.strip())
                    message_element.send_keys(messages[0])
                    message_element.send_keys(Keys.ENTER)
                    driver.implicitly_wait(t)
                    time.sleep(t/2)
                    msgbox = driver.find_element(By.XPATH, ".//div[@role='textbox']")

                    for m in messages[1:]:
                        msgbox.send_keys(m+"\n")
                        time.sleep(t/10)
                    
                    time.sleep(t/2)
                    messaged.append(name)
                    skip.append(name)

                    time.sleep(random.randint(1, t))
                    no_of_dms += 1
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(random.randint(1, t))
                    break
                except Exception as e:
                    pass
            servers = WebDriverWait(driver, 3*t).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Servers']/div")))
    print(messaged)
    return no_of_dms

