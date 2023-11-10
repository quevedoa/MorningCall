import csv
import logging
import requests
from bs4 import BeautifulSoup
from newspaper import Config, Article
import time
import re

urls = ['https://www.elfinanciero.com.mx/economia/',
'https://www.elfinanciero.com.mx/mercados/']

url_stub = 'https://www.elfinanciero.com.mx' # BeautifulSoup jala links relativos, agregamos el stub para hacerlo absoluto
user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

config = Config()
config.browser_user_agent = user_agent_string
headers = {'User-Agent': user_agent_string}

csv_file_name = 'articulos.csv'

# Descomenta la siguiente linea si no sabes wtf going on
# logging.basicConfig(level=logging.DEBUG)

with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    article_count = 1
    for url in urls:
        response = requests.get(url, headers=headers)
        html_pagina = response.content
        soup = BeautifulSoup(html_pagina, 'html.parser')

        divs = soup.find_all('div', class_='results-list--headline-container')
        links_articulos = []

        # Iterate through each 'div' to find 'a' tags and extract 'href'.
        for div in divs:
            a_tag = div.find('a')  # Find the 'a' tag within the 'div'.
            if a_tag and a_tag.has_attr('href'):
                links_articulos.append(a_tag['href'])  # Get the 'href' attribute.

        divs = soup.select('a.simple-list-headline-anchor')

        for div in divs:
           links_articulos.append(div['href'])  # Get the 'href' attribute.

        divs = soup.select('a.sm-promo-headline')

        for div in divs:
           links_articulos.append(div['href'])  # Get the 'href' attribute.

        for link in links_articulos:
            try:
                url = url_stub + link
                article = Article(url, config=config)
                article.download()
                article.parse()

                titulo = article.title
                fecha = str(article.publish_date)
                texto = re.sub(r'[^\S ]+', '', article.text)

                writer.writerow([titulo, fecha, texto, url])
                print(f"Article ({article_count}): {titulo} - {url}")
                article_count += 1
            except Exception as e:
                print(f"Valio verga {url}: {e}")

print(f"SUCCESS. Se guardo todo en {csv_file_name}")
