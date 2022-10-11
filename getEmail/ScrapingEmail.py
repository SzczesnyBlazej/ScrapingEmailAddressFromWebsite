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
            result = requests.get("https://www.google.com/", proxies=proxy, timeout=3
                                  )
            if result.status_code == 200:
                working.append(proxy)

        except:
            pass
    print((len(working) / 200) * 100, "working proxy")
    return working


start_time = time.time()
# proxies = getProxies()
#
# workingProxies = getWorkingProxies()
workingProxies = [{'https': '14.140.131.82:3128'}, {'https': '186.67.158.61:999'}, {'https': '157.100.12.138:999'},
                  {'https': '116.58.254.126:8080'}, {'https': '189.173.168.174:999'}, {'https': '145.40.121.101:3128'},
                  {'https': '193.164.133.46:3128'}, {'https': '103.60.26.178:3128'}, {'https': '95.217.190.230:80'},
                  {'https': '173.212.200.30:3128'}, {'https': '189.173.168.174:999'}, {'https': '35.233.30.201:3128'},
                  {'https': '173.212.200.30:3128'}, {'https': '193.164.133.46:3128'}, {'https': '35.233.30.201:3128'},
                  {'https': '95.217.190.230:80'}, {'https': '103.125.162.134:83'}, {'https': '192.99.182.243:3128'},
                  {'https': '157.100.12.138:999'}, {'https': '35.233.30.201:3128'}, {'https': '157.100.12.138:999'},
                  {'https': '189.173.168.174:999'}, {'https': '193.164.133.46:3128'}, {'https': '103.159.168.80:3128'},
                  {'https': '193.122.71.184:3128'}, {'https': '193.164.133.46:3128'}, {'https': '103.159.168.80:3128'},
                  {'https': '173.212.200.30:3128'}, {'https': '35.233.30.201:3128'}, {'https': '116.58.254.126:8080'},
                  {'https': '193.122.71.184:3128'}, {'https': '189.173.168.174:999'}, {'https': '189.173.168.174:999'},
                  {'https': '157.100.12.138:999'}, {'https': '189.173.168.174:999'}, {'https': '157.100.12.138:999'},
                  {'https': '173.212.200.30:3128'}, {'https': '136.226.10.111:9480'}, {'https': '189.173.168.174:999'},
                  {'https': '116.58.254.126:8080'}, {'https': '190.121.157.142:999'}]

if (len(workingProxies) < 3):
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
    for pageNumber in range(31, 32):
        valid = False
        while not valid:
            try:
                proxy = choice(workingProxies)
                url = "https://welcome2poland.eu/firmy/polska/meble%20-%20kuchenne?page=" + str(pageNumber)
                result = requests.get(url, proxies=proxy, headers={'User-Agent': 'Chrome'}, timeout=3)
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
                result = requests.get(url, proxies=proxy, headers={'User-Agent': 'Chrome'}, timeout=3)
                if result.ok:
                    counter += 1
                    soup = bs(result.content, 'lxml')
                    item = soup.find_all('li', attrs={"class": "company-email"})
                    if len(item) == 0:
                        print("Brak podanego adresu email")
                    else:
                        for x in item:
                            tempEmail = x.find('a')['href'][7:]
                            print("Email", counter, ":", tempEmail)
                            if not tempEmail in emailAddr:
                                emailAddr.append(tempEmail)
                        time.sleep(round(random.uniform(0.6, 1.2), 2))
                    valid = True

                else:
                    pass
            except:
                print("connection error, trying again....")
                pass
    print(emailAddr)
    print(len(emailAddr))
    print("--- %s seconds ---" % (time.time() - start_time))
    print(round((time.time() - start_time) / len(emailAddr), 2), "- time to search one email address")


getLinksFromPagesRange()
