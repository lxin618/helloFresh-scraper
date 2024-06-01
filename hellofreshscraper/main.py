import json
import os
import re
from os.path import basename

import requests
from bs4 import BeautifulSoup

# Opening JSON file
f = open('data.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data['urlset']['url']:
    # Send an HTTP request to the URL of the webpage you want to access
    response = requests.get(i['loc'])
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # # Extract the text content of the webpage
    title = soup.find("h1", class_='sc-a6821923-0 ceYciq', attrs={"data-zest": "hellofresh"}).text
    subtitle = soup.find("h2", class_='sc-a6821923-0 jECFqG', attrs={"data-zest": "hellofresh"}).text

    description = soup.find("span", attrs={"data-test-id": "description-body-title"}).find_all('p')
    recipeDescription = description[0].text
    calDescription = description[1].text if 1 < len(description) else None

    tags = []
    items = soup.find_all("div", class_="sc-a6821923-0 HzHkS", attrs={"data-test-id": "recipe-description-tag"})
    for item in items:
        spans = item.find_all('span')
        for span in spans:
            if span.text != '•':
                tags.append(span.text)

    timeNdiffArray = {}
    timeNdiff = soup.find(class_="sc-a6821923-0 kuiNX")
    values = timeNdiff.find_all('span', class_='sc-a6821923-0 eZjiGJ')
    for index, i in enumerate(values):
        if index == 0:
            timeNdiffArray['time'] = i.text
        elif index == 1:
            timeNdiffArray['difficulty'] = i.text

    nutrition = {}
    nuts = soup.find("div", class_="sc-a6821923-0 jCgtKL", attrs={'data-test-id':'items-per-serving'})
    steps = nuts.find_all('div', attrs={'data-test-id': 'nutrition-step'}, class_='sc-a6821923-0 kimgtP')
    for item in steps:
        key = item.find('span', class_='sc-a6821923-0 kUCRYF').text
        value = item.find('span', class_='sc-a6821923-0 eZjiGJ').text
        nutrition[key] = value

    ingredients = {}
    ings = soup.find_all('div', class_='sc-a6821923-0 eOyORz', attrs={'data-test-id': 'ingredient-item-shipped'})
    for ing in ings:
        # ingredients image
        ingImage = ing.find('div', class_='sc-a6821923-0 hZWAJE')
        ingSrc = ingImage.img['src']
        name = ingImage.img['alt']
        path = os.path.join(title.lower(), 'ingredients')
        os.mkdir(path)
        with open(title.lower() + '/ingredients/'+name.lower(), "wb") as f:
            f.write(requests.get(ingSrc).content)
        texts = ing.find('div', class_='sc-a6821923-0 frRfTC')
        howmuch = texts.find('p', class_='sc-a6821923-0 bNkKoC').text
        what = texts.find('p', class_='sc-a6821923-0 fLfTya').text
        ingredients['imagesrc'] = ingSrc
        ingredients['name'] = howmuch+' '+what

    break

# Closing file
f.close()