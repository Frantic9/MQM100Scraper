import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

f = open("Links.txt", "a")
print("How many Links you want?")
size = input()
len = int(size)
ref_array = []



def render_page(url):
    path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get(url)
    time.sleep(1)
    r = driver.page_source
    return r


for x in range(len):
    goog_search = "https://randomrepo.com/"

    r  = render_page(goog_search)

    soup = BeautifulSoup(r, "html.parser")
    soup = soup.find("div", {"class": "col-12 text-center"}).find("a")
    ref = soup.get("href")
    ref_array.append(ref)

for x in range(len):
    for j in range(x+1,len):
        if(ref_array[x] == ref_array[j]):
            goog_search = "https://randomrepo.com/"
            r  = render_page(goog_search)
            soup = BeautifulSoup(r, "html.parser")
            soup = soup.find("div", {"class": "col-12 text-center"}).find("a")
            ref = soup.get("href")
            ref_array[j] = ref


for x in range(len):
    f.write(ref_array[x])
    f.write("\n")
f.close()
