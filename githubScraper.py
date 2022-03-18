from bs4 import BeautifulSoup
import requests
import xlsxwriter

#Reads urls from file
def read_file(file):
    f = open(file,"r")
    links = []

    for x in f:
        links.append(x.strip())
    f.close()
    return links

def get_data(url):
    page = requests.get(url)
    if page.status_code != 200:
        print("Page at " + url + " not responding")
        exit(1)
    soup = BeautifulSoup(page.text, "html.parser")
    
    stars = process_data(soup, 3)
    watching = process_data(soup, 4)
    forks = process_data(soup, 5)

    print(stars + " stars")
    print(watching + " watching")
    print(forks + " forks")

def process_data(soup, type):
    final_string = soup.find_all('a',{"class": "Link--muted"})[type].get_text()
    temp_string = ""
    for i in final_string:
        if not i.isalpha():
            temp_string += i
        if i == 'k':
            temp_string += i
            break
    final_string = temp_string.strip()

    return final_string

get_data(read_file("Links.txt")[0])

