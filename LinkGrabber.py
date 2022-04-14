from bs4 import BeautifulSoup
import time
from selenium import webdriver

def render_page(url):
    path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get(url)
    time.sleep(1.5)
    r = driver.page_source
    return r

def get_html():
    goog_search = "https://randomrepo.com/"
    r  = render_page(goog_search)
    soup = BeautifulSoup(r, "html.parser")
    soup = soup.find("div", {"class": "col-12 text-center"}).find("a")
    return soup.get("href")

f = open("Links.txt", "a")
print("How many Links would you like?")
size = input()
len = int(size)
ref_array = []

for x in range(len):
    ref_array.append(get_html())

for x in range(len):
    for j in range(x+1,len):
        if(ref_array[x] == ref_array[j]):
            ref_array[j] = get_html()


for x in range(len):
    f.write(ref_array[x])
    f.write("\n")
f.close()
