import requests
import bs4
from bs4 import BeautifulSoup
import csv
import re

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
r = requests.get(url)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

movies = []

nbOfMovies = len(soup.find_all('td', {'class': 'titleColumn'}))
actors = []
directors = []
countries = []

for i in range(nbOfMovies):

    dictMovie = {"Title": " ", "Year": 0, "Url": "", "Genre": "",
                 "Directors": [], "Countries": [], "Main Actors": []}

    actors_movie = []
    directors_movie = []
    countries_movie = []

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
    country_movie = movieSoup.select(
        'li[data-testid="title-details-origin"]')[-1].text

    director_movie = re.sub("[(*.)]", "", director_movie)
    director_movie = re.sub("uncredited", "", director_movie)
    director_movie = re.sub("co-directed by", "", director_movie)
    director_movie = re.split(
        "(?<=[a-zéè])(?<!Mc)(?=[A-ZÉÈÊ])", director_movie)
    country_movie = re.sub("Country of origin", "", country_movie)
    country_movie = re.sub("Countries of origin", "", country_movie)
    country_movie = re.split("(?<=[a-zéè])(?=[A-ZÉÈÊ])", country_movie)

    dictMovie['Genre'] = genre_movie
    dictMovie['Countries'] = countries_movie
    dictMovie['Directors'] = directors_movie
    dictMovie['Main Actors'] = actors_movie

    nbOfDirectors = len(director_movie)
    nbOfCountries = len(country_movie)

    for y in range(nbOfCountries):
        country = {"Name": " ", "Movies": []}

        country_name = country_movie[y]

        countries_movie.append(country_name)
        country['Name'] = country_name
        country['Movies'].append(title_movie)
        country['Number of Movies'] = len(country['Movies'])

        exists = False

        for dict in countries:
            if dict['Name'] == country_name:
                dict['Movies'].append(title_movie)
                dict['Number of Movies'] = len(dict['Movies'])
                exists = True
                break

        if not exists:
            countries.append(country)

    for x in range(nbOfDirectors):
        dictDirector = {"Name": " ", "Movies": []}

        director_name = director_movie[x]

        directors_movie.append(director_name)
        dictDirector['Name'] = director_name
        dictDirector['Movies'].append(title_movie)
        dictDirector['Number of Movies'] = len(dictDirector['Movies'])

        exists = False

        for dict in directors:
            if dict['Name'] == director_name:
                dict['Movies'].append(title_movie)
                dict['Number of Movies'] = len(dict['Movies'])
                exists = True
                break

        if not exists:
            directors.append(dictDirector)

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

    movies.append(dictMovie)


with open('Top250Movies.csv', 'w', newline="", encoding='utf-8') as f:
    cols = ['Title', 'Year', 'Url', 'Genre',
            'Countries', 'Directors', 'Main Actors']
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    writer.writerows(movies)

with open('Top250Movies-Actors.csv', 'w', newline="", encoding='utf-8') as f2:
    cols = ['Name', 'Movies', 'Number of Movies', 'Url']
    writer = csv.DictWriter(f2, fieldnames=cols)
    writer.writeheader()
    writer.writerows(actors)

with open('Top250Movies-Directors.csv', 'w', newline="", encoding='utf-8') as f3:
    cols = ['Name', 'Movies', 'Number of Movies']
    writer = csv.DictWriter(f3, fieldnames=cols)
    writer.writeheader()
    writer.writerows(directors)

with open('Top250Movies-Countries.csv', 'w', newline="", encoding='utf-8') as f4:
    cols = ['Name', 'Movies', 'Number of Movies']
    writer = csv.DictWriter(f4, fieldnames=cols)
    writer.writeheader()
    writer.writerows(countries)
