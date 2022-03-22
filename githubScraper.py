from bs4 import BeautifulSoup
import requests
import xlsxwriter

#Reads urls from file and returns them in an array
def read_file(file):
    f = open(file,"r")
    links = []

    for x in f:
        links.append(x.strip())
    f.close()
    return links

#grabs data from each github url
def get_data(url):
    page = requests.get(url)
    if page.status_code != 200:
        print("Page at " + url + " not responding")
        exit(1)
    soup = BeautifulSoup(page.text, "html.parser")

    data = process_data(soup)
    
    print("Stars: " + data[0])
    print("Watching: " + data[1])
    print("Forks: " + data[2])
    print("Issues: " + data[3])
    print("Contributors: " + data[4])
    print("Main Language: " + data[5])

    return data

#parses each string to get formatted data
def process_data(soup):
    length = len(soup.find_all('a',{"class": "Link--muted"}))
    return_data = []
    #Stars, Watching, and Forks
    for i in range(length - 3, length):
        return_data.append(filter_number(soup.find_all('a',{"class": "Link--muted"})[i].get_text()))
    
    #Issues
    try:
        return_data.append(filter_number(soup.find('a',{"id": "issues-tab"}).getText()))
    except:
        return_data.append("0");

    #Contributors
    cont = soup.find_all('a', {"class" : "Link--primary no-underline"})
    return_data.append(filter_number(cont[len(soup.find_all('a', {"class" : "Link--primary no-underline"})) - 1].get_text()))

    #Main Language
    try:
        return_data.append(soup.find('a', {"class" : "d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3"}).get_text().strip())
    except:
        return_data.append("No Langauge Detected")

    return return_data

def filter_number(input):
    input.strip()
    temp_string = ""
    for x in input:
        if not x.isalpha() and x != '\n' and x != ' ':
            temp_string += x
        elif x == 'k': 
            temp_string += x
            break
        elif x == 'f':
            break
    return temp_string.strip()

#TODO Write this still
def excel_plotter(data):
    print("A")

data_list = []
for url in read_file("Links.txt"):
    print(url)
    data_list.append(get_data(url))
    print()