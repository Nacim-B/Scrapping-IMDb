import requests
import bs4
from bs4 import BeautifulSoup
import csv

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
r = requests.get(url)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

movies_array = []

nbOfMovies = len(soup.find_all('td', {'class': 'titleColumn'}))
actors = []

for i in range(nbOfMovies):

    dictMovie = {}

    actors_movie = []
    directors_movie = []

    title_movie = soup.find_all('td', {'class': 'titleColumn'})[
        i].find_all('a')[-1].text
    year_movie = soup.find_all('td', {'class': 'titleColumn'})[i].find_all(
        'span', {'class': 'secondaryInfo'})[-1].text.replace('(', '').replace(')', '')
    url_movie = 'https://imdb.com' + \
        soup.find_all('td', {'class': 'titleColumn'})[i].a['href']

    dictMovie['Title'] = title_movie
    dictMovie['Year'] = year_movie
    dictMovie['Url'] = url_movie

    moviereq = requests.get(url_movie)
    movieSoup = bs4.BeautifulSoup(moviereq.text, 'html.parser')

    genre_movie = movieSoup.find_all(
        'li', {'class': 'ipc-inline-list__item ipc-chip__text'})[-1].text
    director_movie = movieSoup.find_all(
        'div', {'class': 'ipc-metadata-list-item__content-container'})[0].text

    dictMovie['Genre'] = genre_movie
    dictMovie['Director'] = director_movie
    dictMovie['Main Actors'] = actors_movie

    nbOfActors = len(movieSoup.find_all('a', {'class': 'sc-36c36dd0-1 QSQgP'}))

    for n in range(nbOfActors):
        if n < 10:
            actor_url = 'https://imdb.com'+movieSoup.find_all(
                'div', {'class': 'sc-36c36dd0-8 fSYMLK'})[n].a['href']
            actor_name = movieSoup.find_all(
                'a', {'class': 'sc-36c36dd0-1 QSQgP'})[n].text

            actors_movie.append(actor_name)

            actor = {"Name": " ", "Movies": []}
            actor['Name'] = actor_name
            actor['Movies'].append(title_movie)
            actor['Number of Movies'] = len(actor['Movies'])
            actor['Url'] = actor_url

            exists = False

            for dict in actors:
                if dict['Name'] == actor_name:
                    dict['Movies'].append(title_movie)
                    dict['Number of Movies'] = len(dict['Movies'])
                    exists = True
                    break

            if not exists:
                actors.append(actor)

    movies_array.append(dictMovie)

with open('Top250Movies.csv', 'w', newline="", encoding='utf-8') as f:
    cols = ['Title', 'Year', 'Url', 'Genre', 'Director', 'Main Actors']
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    writer.writerows(movies_array)

with open('Top250Movies-Actors.csv', 'w', newline="", encoding='utf-8') as f:
    cols = ['Name', 'Movies', 'Number of Movies', 'Url']
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    writer.writerows(actors)
