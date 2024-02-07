import requests
from bs4 import BeautifulSoup
from newspaper import Config, Article
import re
import json
import subprocess

print("Scraping...")

news_stubs = {
    'elceo': ['https://elceo.com/negocios/',
              'https://elceo.com/mercados/',
              'https://elceo.com/economia/'],
    'eleconomista': ['https://www.eleconomista.com.mx/seccion/empresas',
                     'https://www.eleconomista.com.mx/seccion/economia',
                     'https://www.eleconomista.com.mx/seccion/mercados',
                     'https://www.eleconomista.com.mx/seccion/sectorfinanciero',
                     'https://www.eleconomista.com.mx/seccion/estados',
                     'https://www.eleconomista.com.mx/seccion/politica',
                     'https://www.eleconomista.com.mx/seccion/energia',
                     'https://www.eleconomista.com.mx/seccion/internacionales',
                     'https://www.eleconomista.com.mx/seccion/tecnologia',
                     'https://www.eleconomista.com.mx/seccion/estados'], 
    'elfinanciero': ['https://www.elfinanciero.com.mx/economia/',
                     'https://www.elfinanciero.com.mx/mercados/'],
    'forbes': ['https://www.forbes.com.mx/negocios/',
               'https://www.forbes.com.mx/economia-y-finanzas/']
}

url_stub = 'https://www.eleconomista.com.mx/seccion' # BeautifulSoup jala links relativos, agregamos el stub para hacerlo absoluto
user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' # Si no los robots.txt se vuelven locos

config = Config()
config.browser_user_agent = user_agent_string
headers = {'User-Agent': user_agent_string}

parsed_urls_file_name = '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/VMPipeline/ScrapingScripts/parsed_urls.txt'

# Checa todos los urls que ya leyó
link_set = set()
with open(parsed_urls_file_name,'r') as file:
    for line in file:
        url = line.strip()
        if url:
            link_set.add(url)

articulos_nuevos = []

def get_elceo_articles():
    new_urls = []

    stubs = news_stubs['elceo']
    for url in stubs:
        response = requests.get(url, headers=headers)
        html_pagina = response.content

        soup = BeautifulSoup(html_pagina, 'html.parser')
        links_articulos = soup.select('a.post-link') # Esto solo jala para elceo, jala todos los a tags con clase 'post-link' 

        for link in links_articulos:
            try:
                article_url = link.get('href')
                if article_url not in link_set:
                    link_set.add(article_url)
                    new_urls.append(article_url)

                    article = Article(article_url, config=config)
                    article.download()
                    article.parse()

                    titulo = article.title
                    fecha = str(article.publish_date)
                    texto = re.sub(r'[^\S ]+', '', article.text)

                    new_article = {
                        'titulo': titulo,
                        'fecha': fecha,
                        'texto': texto,
                        'url': article_url,
                        'source': 'El CEO'
                    }
                    articulos_nuevos.append(new_article)

                    print(f"{titulo} agregado.")

            except Exception as e:
                print(f"Valio verga {url}: {e}")

def get_eleconomista_articles():
    new_urls = []

    stubs = news_stubs['eleconomista']
    for url in stubs:
        response = requests.get(url, headers=headers)
        html_pagina = response.content

        soup = BeautifulSoup(html_pagina, 'html.parser')
        links_articulos = soup.select('a.jsx-578919967') # Esto solo jala para eleconomista

        for link in links_articulos:
            try:
                relative_url = link.get('href')
                article_url = url_stub + relative_url
                if article_url not in link_set:
                    link_set.add(article_url)
                    new_urls.append(article_url)

                    article = Article(article_url, config=config)
                    article.download()
                    article.parse()

                    titulo = article.title
                    fecha = str(article.publish_date)
                    texto = re.sub(r'[^\S ]+', '', article.text)

                    new_article = {
                        'titulo': titulo,
                        'fecha': fecha,
                        'texto': texto,
                        'url': article_url,
                        'source': 'El Economista'
                    }
                    articulos_nuevos.append(new_article)
            except Exception as e:
                print(f"Valio verga {url}: {e}")

def get_elfinanciero_articles():
    new_urls = []

    stubs = news_stubs['elfinanciero']
    for url in stubs:
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
                article_url = url_stub + link
                if article_url not in link_set:
                    link_set.add(article_url)
                    new_urls.append(article_url)

                    article = Article(article_url, config=config)
                    article.download()
                    article.parse()

                    titulo = article.title
                    fecha = str(article.publish_date)
                    texto = re.sub(r'[^\S ]+', '', article.text)

                    new_article = {
                        'titulo': titulo,
                        'fecha': fecha,
                        'texto': texto,
                        'url': article_url,
                        'source': 'El Financiero'
                    }
                    articulos_nuevos.append(new_article)
            except Exception as e:
                print(f"Valio verga {url}: {e}")

def get_forbes_articles():
    new_urls = []

    stubs = news_stubs['forbes']
    for url in stubs:
        response = requests.get(url, headers=headers)
        html_pagina = response.content

        soup = BeautifulSoup(html_pagina, 'html.parser')

        divs = soup.find_all('div', class_='f4_segment__block__right')
        links_articulos = []

        # Iterate through each 'div' to find 'a' tags and extract 'href'.
        for div in divs:
            a_tag = div.find('h3')  # Find the 'a' tag within the 'div'.
            a_tag = a_tag.find('a')
            if a_tag and a_tag.has_attr('href'):
                links_articulos.append(a_tag['href'])  # Get the 'href' attribute.

        divs = soup.find_all('article', class_='f4_category-header__top__left__article')

        # Iterate through each 'div' to find 'a' tags and extract 'href'.
        for div in divs:
            a_tag = div.find('h2')  # Find the 'a' tag within the 'div'.
            a_tag = a_tag.find('a')
            if a_tag and a_tag.has_attr('href'):
                links_articulos.append(a_tag['href'])  # Get the 'href' attribute.

        for article_url in links_articulos:
            if article_url not in link_set:
                try:
                    link_set.add(article_url)
                    new_urls.append(article_url)

                    article = Article(article_url, config=config)
                    article.download()
                    article.parse()

                    titulo = article.title
                    fecha = str(article.publish_date)
                    texto = re.sub(r'[^\S ]+', '', article.text)

                    new_article = {
                        'titulo': titulo,
                        'fecha': fecha,
                        'texto': texto,
                        'url': article_url,
                        'source': 'Forbes'
                    }
                    articulos_nuevos.append(new_article)
                except Exception as e:
                    print(f"Valio verga {url}: {e}")

get_elceo_articles()
# get_eleconomista_articles()
# get_elfinanciero_articles()
# get_forbes_articles()

with open(parsed_urls_file_name, 'a') as file:
    for articulo in articulos_nuevos:
        file.write(f"{articulo['url']}\n")

subprocess.run(['python3', '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/VMPipeline/clasificador_industria.py'], input=json.dumps(articulos_nuevos), text=True)
