import random
from multiprocessing import Pool
import lxml
from bs4 import BeautifulSoup as bs
import requests
from random import choice
import time

def getProxies():
    # proxyUrl="https://github.com/clarketm/proxy-list/blob/master/proxy-list-raw.txt"
    # proxyUrl = "https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt"
    proxyUrl = "https://github.com/mertguvencli/http-proxy-list/blob/main/proxy-list/data.txt"
    result = requests.get(proxyUrl)
    soup = bs(result.content, "lxml").find_all("td", {"class": "blob-code blob-code-inner js-file-line"})
    proxies = [proxy.text for proxy in soup]
    return proxies


def getRandomProxies(proxies):
    return {"https": choice(proxies)}


def getWorkingProxies():
    working = []
    count = 0
    print("finding working proxy...")
    for i in range(200):
        proxy = getRandomProxies(proxies)
        count += 1
        try:
            result = requests.get("https://www.google.com/", proxies=proxy, timeout=1.5
                                  )
            if result.status_code == 200:
                working.append(proxy)

        except:
            pass
    print((len(working) / 200) * 100, "working proxy")
    return working

start_time = time.time()
proxies = getProxies()

workingProxies = getWorkingProxies()
if(len(workingProxies)<3):
    exit(1)
print(workingProxies)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
listOfAllLinks = []



def getHrefFromList(links):
    listOfHref = []
    for link in links[:10]:
        listOfHref.append(link.find('a')['href'])
    return listOfHref


def getLinksFromPagesRange():
    for pageNumber in range(31, 51):
        valid = False
        while not valid:
            try:
                proxy = choice(workingProxies)
                url = "https://welcome2poland.eu/firmy/polska/meble%20-%20kuchenne?page=" + str(pageNumber)
                result = requests.get(url, proxies=proxy, headers=headers)
                if result.ok:
                    soup = bs(result.text, 'lxml')
                    item = soup.find_all('h3', attrs={"class": "company-name"})

                    getHrefFromList(item)
                    for elem2 in getHrefFromList(item):
                        listOfAllLinks.append(elem2)
                    time.sleep(0.5 + round(random.uniform(0.2, 0.7), 2))
                    valid = True
                else:
                    pass
            except:
                print("connection error, trying again....")
                pass
    getEmailAddrFromLinks()


def getEmailAddrFromLinks():
    emailAddr = []
    counter = 0
    for link in listOfAllLinks:
        valid = False
        while not valid:
            try:
                proxy = choice(workingProxies)
                url = "https://welcome2poland.eu/" + str(link)
                result = requests.get(url, proxies=proxy, headers=headers)
                if result.ok:
                    counter += 1
                    print("Success")
                    soup = bs(result.content, 'lxml')
                    item = soup.find_all('li', attrs={"class": "company-email"})
                    for x in item:
                        print("Email", counter, ":", x.find('a')['href'][7:])
                        emailAddr.append(x.find('a')['href'][7:])
                    time.sleep(0.5 + round(random.uniform(0.2, 0.7), 2))
                    valid = True
                else:
                    pass
            except:
                print("connection error, trying again....")
                pass
    print(emailAddr)
    print(len(emailAddr))
    print("--- %s seconds ---" % (time.time() - start_time))
    print(round((time.time() - start_time) / len(emailAddr),2), "- time to search one email address")


getLinksFromPagesRange()
