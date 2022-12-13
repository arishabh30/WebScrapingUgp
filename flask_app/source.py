from pickle import APPEND
# import pandas as pd
import re
import requests
import time
import array as arr
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import request
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from fake_useragent import UserAgent

def gettingUrl(url):
    # ua=UserAgent()
    # userAgent=ua.random
    options = Options()
    options.headless=True
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--lang=en_US')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent=[userAgent]")
    options.add_argument("--disable-dev-shm-usage")
    
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.get(url)
    html = browser.page_source
    # currentURL = browser.current_url
    print("URL "+url)
    return html


    
# def countAllLinksACS(html):
#     soup2 = BeautifulSoup(html,'html.parser')
#     a_tags = soup2.find('div', class_="article_content-left ui-resizable")
#     paperLinksgoogleScholar=a_tags.find_all('a',class_="google-scholar")  # creating a list containing the google scholar links for all the reference papers.
#     scholarLinks=[]
#     for link in paperLinksgoogleScholar:
#         scholarLinks.append(link['href'])  #A new list containing the google scholar links for only the first three papers is created. 
#     return scholarLinks


# def TitleAcs(html):
#     titleAll = []
#     soup = BeautifulSoup(html,'html.parser')
#     content = soup.find('ol', class_='useLabel')
#     titles = content.find_all('span', class_="NLM_article-title")
#     i=0
#     for t in titles:
#         titleAll.append(titles[i].text)
#         i=i+1
#     return titleAll
# def AcsDoi(html):
#     dois =[]
#     soup = BeautifulSoup(html,'html.parser')
#     content = soup.find('ol', class_='useLabel')
#     doi = content.find_all('span', class_='refDoi')
#     i=0
#     for d in doi:
#         x = re.findall("(?<=DOI\: )(.*)", doi[i].text)
#         new = "https://doi.org/"
#         var = ' '.join(x)
#         dois.append("".join([new,var]))
#         i=i+1
#     return dois
# def AcsYear(html):
#     years =[]
#     soup = BeautifulSoup(html,'html.parser')
#     content = soup.find('ol', class_='useLabel')
#     year = content.find_all('span', class_='NLM_year')
#     i=0
#     for y in year:
#         years.append(year[i].text)
#         i=i+1
#     return years
    
# def AcsJournal(html):
#     journal =[]
#     soup = BeautifulSoup(html,'html.parser')
#     content = soup.find('ol', class_='useLabel')
#     journalList = content.find_all('span', class_='citation_source-journal')
#     i=0
#     for j in journalList:
#         journal.append(journalList[i].text)
#         i=i+1
#     return journal

# def authorNames(citeArray,url):
#     html = gettingUrl(url)
#     count = len(citeArray)
#     soup3 = BeautifulSoup(html, 'html.parser')
#     relevant = soup3.find('div', class_="article_content-left ui-resizable")
#     string_Refs = relevant.find('p', class_="references-count")
#     string = string_Refs.text
#     number_Refs = re.findall(r'\d+', string)
#     i=0
#     allLastAuthors =[]
#     for i in range(1, int(number_Refs[0])+1):

#         info = relevant.find('li', {"id":"ref"+str(i)})

#         if info is None:
#             continue

#         authors = info.find_all('span',class_='NLM_contrib-group')
#         last_author = authors[-1].text
#         allLastAuthors.append(last_author)

#     return allLastAuthors




def Nature(html):
    # Extraction from "Nature" publication house.
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find('ol', class_="c-article-references")
    tags = links.find_all('a', {'data-track-action': 'google scholar reference'})
    # to get the google scholar links of the references.
    paperLinksgoogleScholarnature = []
    for tag in tags:
        # creating a list containing the google scholar links for all the
        paperLinksgoogleScholarnature.append(tag['href'])


    # to get the doi of the references.
    natureDOI = []
    refNumber = len(paperLinksgoogleScholarnature)

    i=0

    for i in range(1, int(refNumber)+1):
        doiLinks = links.find('a', {'aria-label': 'Article reference '+str(i)})

        if doiLinks == None:
            natureDOI.append("No DOI")
        else:
            natureDOI.append(doiLinks['href'])
        i+=1
    

    # extracting the authors from the main page itself.
    text = soup.find_all('ol', class_='c-article-references')
    # print(text)
    text_main = soup.find_all(
        'li', class_='c-article-references__item js-c-reading-companion-references-item')
    # print(text_main[0])

    Titles = []
    allLastAuthors = []
    journalName = []
    yearPublication = []

    for ref in text_main:
        string = ref.find('p', class_='c-article-references__text')

        togetdeets = string.text.split('.')

        # returns authors in the form of a string.
        allAuthors = togetdeets[0]
        allAuthorsList = allAuthors.split(',')  # converting to a list

        Titles.append(togetdeets[1])  # gets the title of the references
        
        journal = togetdeets[2].split(';')
        journalName.append(journal[0])# gets the journal name of the references

        if len(togetdeets) < 4:
            yearPublication.append(' ') #gets the year of publication of the references
        else:
            year = togetdeets[3].split(';')
            yearPublication.append(year[0]) #gets the year of publication of the references

        if allAuthorsList[-1] == ' et al':
            allLastAuthors.append(allAuthorsList[-2])
        else:
            allLastAuthors.append(allAuthorsList[-1])
        
    return allLastAuthors, Titles, journalName, yearPublication, natureDOI, paperLinksgoogleScholarnature



def Springer(html):
    # Extraction from "Springer" publication house.
# html = gettingUrl("https://link.springer.com/article/10.1007/s43673-022-00064-1")
    paperLinksgoogleScholar = []

# creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('ol', class_="c-article-references")
    refNumber = len(links)
    k = 0
    for k in range(1, int(refNumber)+1):
        tags = links.find('a', {'aria-label': 'Google Scholar reference ' +str(k)})
        if tags==None:
            paperLinksgoogleScholar.append("No Google Scholar Link")
        else:
            paperLinksgoogleScholar.append(tags['href'])
        k+=1


    #to get the doi of the references.
    springerDOI = []
    

    i=0

    for i in range(1, int(refNumber)+1):
        doiLinks = links.find('a', {'aria-label': 'Article reference '+str(i)})

        if doiLinks == None:
            springerDOI.append("No DOI")
        else:
            springerDOI.append(doiLinks['href'])
        i+=1

    # print(springerDOI)


    #extracting the authors from the main page itself.
    text = soup.find_all('ol', class_='c-article-references')
    text_main = soup.find_all('li', class_='c-article-references__item js-c-reading-companion-references-item')

    Titles = []
    allLastAuthors = []
    journalName = []
    yearPublication = []

    for ref in text_main:
        string = ref.find('p', class_="c-article-references__text")

        togetdeets = string.text.split(',')
        content = togetdeets[-2].split('.')
        Titles.append(content[0]) # gets the title of the references

        if len(togetdeets)<4:
            allLastAuthors.append("No Data Found")
        else:
            allLastAuthors.append(togetdeets[-3])

        sum = ''
        for j in range(1, len(content)-1):
            sum += content[j]
        journalName.append(sum) # gets the journal name of the references

        year = togetdeets[-1].split('(')
        # print(year[-1])

        if year[-1][0]==" ":
            yearPublication.append("No Data Found") # gets the year of publication of the references
        else:
            year_new = year[-1].split(')')
            yearPublication.append(year_new[0]) #gets the year of publication of the references


    return allLastAuthors, Titles, journalName, yearPublication, springerDOI, paperLinksgoogleScholar

def Science(html):
    # extraction from "Science" publication house.
# html = gettingUrl("https://www.science.org/doi/10.1126/sciadv.abq2104")
    paperLinksgoogleScholar = []
    scienceDOI = []
    toGetDeets = []
    allLastAuthors = []
    journalName = []
    Titles = []
    yearPublication = []
    # creating an instance of the BeautifulSoup library
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find('section', {'id': 'bibliography'})
    forLabels = tags.find_all("div", class_='label')

    refNumber = len(forLabels)

    i=0

    content = tags.find_all('div', class_= "citation")
    for con in content:
        toGetDeets.append(con.find('div', class_='citation-content'))

    for deet in toGetDeets:
        if deet.find('em') == None:
            journalName.append("No Data Found")
        else:
            journalName.append(deet.find('em').text)

    for deet in toGetDeets:
        detail = deet.text.split(',')
        if ('(' in detail[-1]) == False:
            yearPublication.append("No Data Found")
        else:
            yearPublication.append(detail[-1].split('(')[-1].split(')')[0])

    for deet in toGetDeets:
        Titles.append(deet.text)

    for con in content:
        link = con.find('a')
        if link.text == "Crossref":
            scienceDOI.append(link['href'])
        else:
            scienceDOI.append("No DOI")

    for con in content:
        link = con.find_all('a')
        if (link[-1].text == "Google Scholar"):
            paperLinksgoogleScholar.append(link[-1]['href'])
        else:
            paperLinksgoogleScholar.append("Google Scholar Link Not Found")

    for i in range(0,refNumber):
        allLastAuthors.append("Next Column for Authors")
    
    return allLastAuthors, Titles, journalName, yearPublication, scienceDOI, paperLinksgoogleScholar


def Publication(link):
    x = re.findall('www\.(.*?)\.', link)
    return x