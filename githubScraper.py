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
        return_data.append(soup.find('a', {"class" : "d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3"}).get_text().strip().replace('\n', " "))
    except:
        return_data.append("No Langauge Detected")

    return return_data

#Filters out numbers from the garbled strings
def filter_number(input):
    input.strip()
    temp_string = ""
    for x in input:
        if not x.isalpha() and x != '\n' and x != ' ':
            temp_string += x
        elif x == 'k': 
            temp_string += x
            break
        #Edge case for forks
        elif x == 'f':
            break
    return temp_string.strip()

#Inputs data into an excel sheet
def excel_plotter(data_list, url):
    workbook = xlsxwriter.Workbook('mqm100data.xlsx')
    worksheet = workbook.add_worksheet()
    
    #Headers for columns
    worksheet.write('A1', 'Github Repo')
    worksheet.write('B1', 'Stars')
    worksheet.write('C1', 'Watching')
    worksheet.write('D1', 'Forks')
    worksheet.write('E1', 'Issues')
    worksheet.write('F1', 'Contributors')
    worksheet.write('G1', 'Main Language')

    #Input data into excel sheet
    row = 1
    for data in data_list:
        col = 1
        for x in data:
            worksheet.write(row, 0, url[row - 1])
            worksheet.write(row, col, x)
            col += 1
        row += 1
    
    workbook.close()

#Formats the data to be in a better format for excel usage
def excel_format(data_list):
    for data in data_list:
        for i in range(5):
            data[i] = data[i].replace('.','')
            data[i] = data[i].replace('k','000')
        data[5] = language_format(data[5])
    return data_list

#Gets rid of the precentage for the language
def language_format(language):
    temp_string = ""
    for char in language:
        if char.isalpha() or char == ' ' or char == '+':
            temp_string += char
    return temp_string.strip()

data_list = []
for url in read_file("Links.txt"):
    print(url)
    data_list.append(get_data(url))
    print()
excel_plotter(excel_format(data_list), read_file("Links.txt"))
