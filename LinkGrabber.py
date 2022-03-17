import requests
from bs4 import BeautifulSoup
import lxml
import time
from selenium import webdriver

f = open("Links.txt", "a")



def render_page(url):
    path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get(url)
    time.sleep(1)
    r = driver.page_source
    return r


for x in range(3):
    goog_search = "https://randomrepo.com/"

    r  = render_page(goog_search)


    soup = BeautifulSoup(r, "html.parser")
    soup = soup.find("div", {"class": "col-12 text-center"}).find("a")
    f.write(soup.get("href"))
    f.write("\n")

f.close()
