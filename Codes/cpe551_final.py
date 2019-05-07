# -*- coding: utf-8 -*-
"""
Created on Sat May  4 18:10:27 2019

@author: Haijun Huang
"""

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Download IMDB's Top 250 data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title').split('(')[0] for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
titles = [' '.join(movie.get_text().split()[1:-1]).replace('.', '') for movie in movies]
years = [int(a.get_text()[1:-1]) for a in soup.select('span.secondaryInfo')]
ratings = list(map(lambda x: round(float(x),1),ratings))

imdb = []

# Store each item into dictionary (data), then put those into a list (imdb)
for index in range(0, len(movies)):
    # Seperate movie into: 'place', 'title', 'year'
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index)) + 1: -7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[: len(str(index)) - (len(movie))]
    data = {"movie_title": movie_title,
            "star_cast": crew[index],
            "rating": ratings[index],
            "link": links[index]}
    imdb.append(data)

movieTime = []
movieCountry = []
for index in range(0, len(movies)):
    print(index)
    url = 'http://www.imdb.com/' + links[index]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    movieTime.append(' '.join(soup.select('div.subtext a')[-1].get_text().split('(')[0]))
    movieCountry.append(soup.select('div.subtext a')[-1].get_text().split('(')[1].strip().strip(')'))
  
    
df = pd.DataFrame()
df['Title'] = titles
df['Country'] = movieCountry
df['Year'] = years
df['Rating'] = ratings
df['Director'] = crew

df.index = np.arange(1,251)
df.to_csv('top_250_movies_data.csv',index = True, encoding='utf_8_sig')

df1 = pd.read_csv('top_250_movies_data.csv')
Counter(df1['Year'],bins = 20)
plt.hist(df1['Year'],bins=20,rwidth = 1)

Counter(df1['Country'], bins = 21)

    