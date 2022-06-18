import os, json, csv, time,random

from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException,ElementNotInteractableException,ElementClickInterceptedException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver import DesiredCapabilities
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

path = os.getcwd()
DRIVER_PATH = path + '/chromedriver'

class Selenium:

    def get_driver(proxy=None):
        options = Options()
        options.headless = False
        options.add_experimental_option( "prefs", {'protocol_handler.excluded_schemes.discord': True})
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names,operating_systems=operating_systems,limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        
        if proxy:

            prox = Proxy()
            prox.proxyType = ProxyType.MANUAL
            prox.autodetect = False
            prox.httpProxy = prox.sslProxy = prox.socksProxy = proxy
            options.Proxy = prox

            capabilities = dict(DesiredCapabilities.CHROME)
            capabilities['proxy'] = {'proxyType':
                'MANUAL','httpProxy': proxy,
                'ftpProxy': proxy,
                'sslProxy': proxy,'noProxy': '',
                'class': "org.openqa.selenium.Proxy",
                'autodetect': False}

        options.add_argument('--disable-gpu')
        options.add_argument("--start-maximized")
        # prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # options.add_argument('--verbose')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument("--disable-notifications")
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('log-level=3')

        if proxy:
            driver = webdriver.Chrome(options=options,executable_path=DRIVER_PATH,desired_capabilities=capabilities)
        else:
            driver = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)

        return driver

def get_proxies():

    proxies = []
    with open(f'{path}/data/proxies.txt') as f:
        for nm,i in enumerate(f.read().split('\n')):
            if i != '':
                proxies.append(i)
    return proxies

def get_split_proxies(nprocess,nthreads,proxies):

    #proxies split
    proxies_split = {}
    size = int(len(proxies)//nprocess)
    for i in range(1,nprocess+1):

        proxies_split[i] = []
        if i < nprocess:
            da = proxies[(i-1)*size : size * i]
        else:
            da = proxies[(i - 1) * size:]

        size2 = int(len(da)//nthreads)

        for x in range(1,nthreads+1):
            if x < nthreads:
                proxies_split[i].append(da[(x-1)*size2 : size2 * x])
            else:
                proxies_split[i].append(da[(x - 1) * size2:])

    return proxies_split


def get_emails(nprocess,nthreads):

    accounts = []
    with open(f'{path}/data/accounts.txt') as f:
        for nm,i in enumerate(f.read().split('\n')):
            if i != '':
                accounts.append([i.split(' ')[0],i.split(' ')[1],i.split(' ')[-1]])


    accounts_split = {}
    size = int(len(accounts)//nprocess)
    for i in range(1,nprocess+1):

        accounts_split[i] = []
        if i < nprocess:
            da = accounts[(i-1)*size : size * i]
        else:
            da = accounts[(i - 1) * size:]

        size2 = int(len(da)//nthreads)

        for x in range(1,nthreads+1):
            if x < nthreads:
                accounts_split[i].append(da[(x-1)*size2 : size2 * x])
            else:
                accounts_split[i].append(da[(x - 1) * size2:])

    return accounts_split


def get_messages():

    messages = []

    with open(f'{path}/data/messages.txt') as f:
        for nm,i in enumerate(f.read().split('\n')):
            if i != '':
                messages.append(i)

    return messages
