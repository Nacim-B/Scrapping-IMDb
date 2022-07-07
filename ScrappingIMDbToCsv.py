import requests
import bs4
from bs4 import BeautifulSoup
import csv

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
r = requests.get(url)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

movies_array = []

nbOfMovies = len(soup.find_all('td', {'class': 'titleColumn'}))

for i in range(nbOfMovies):
    dictMovie = {}
    actors = []

    dictMovie['Title'] = soup.find_all('td', {'class': 'titleColumn'})[
        i].find_all('a')[-1].text

    dictMovie['Year'] = soup.find_all('td', {'class': 'titleColumn'})[i].find_all('span',{'class': 'secondaryInfo'})[-1].text.replace('(', '').replace(')', '')

    dictMovie['Url'] = 'https://imdb.com' + \
        soup.find_all('td', {'class': 'titleColumn'})[i].a['href']

    tempreq = requests.get(dictMovie['Url'])
    tempSoup = bs4.BeautifulSoup(tempreq.text, 'html.parser')

    dictMovie['Genre'] = tempSoup.find_all(
        'li', {'class': 'ipc-inline-list__item ipc-chip__text'})[-1].text
    dictMovie['Director'] = tempSoup.find_all(
        'div', {'class': 'ipc-metadata-list-item__content-container'})[0].text
    dictMovie['Actors'] = actors

    nbOfActors = len(tempSoup.find_all('a', {'class': 'sc-36c36dd0-1 QSQgP'}))

    for n in range(nbOfActors):
        actors.append(tempSoup.find_all(
            'a', {'class': 'sc-36c36dd0-1 QSQgP'})[n].text)

    movies_array.append(dictMovie)

with open('Top250MoviesV2.csv', 'w', newline="", encoding='utf-8') as f:
    cols = ['Title', 'Year', 'Url', 'Genre', 'Director', 'Actors']
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    writer.writerows(movies_array)
