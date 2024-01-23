import csv
import logging
import requests
from bs4 import BeautifulSoup
from newspaper import Config, Article
import re

urls = ['https://www.forbes.com.mx/negocios/',
'https://www.forbes.com.mx/economia-y-finanzas/']

user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

config = Config()
config.browser_user_agent = user_agent_string
headers = {'User-Agent': user_agent_string}

# csv_file_name = 'articulos.csv'
csv_file_name = '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/CSVDeArticulos/articulos_forbes.csv'
parsed_urls_file_name = '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/parsed_urls.txt'

# Descomenta la siguiente linea si no sabes wtf going on
# logging.basicConfig(level=logging.DEBUG)

# Checa todos los urls que ya leyó
url_set = set()
with open(parsed_urls_file_name,'r') as file:
    for line in file:
        url = line.strip()
        if url:
            url_set.add(url)

article_count = 0
with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    new_urls = []
    for url in urls:
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

        for link in links_articulos:
            if link not in url_set:
                try:
                    url_set.add(link)
                    new_urls.append(link)

                    article = Article(link, config=config)
                    article.download()
                    article.parse()

                    titulo = article.title
                    fecha = str(article.publish_date)
                    texto = re.sub(r'[^\S ]+', '', article.text)

                    writer.writerow([titulo, fecha, texto, link])
                    article_count += 1
                    print(f"Article ({article_count}): {titulo} - {link}")
                except Exception as e:
                    print(f"Valio verga {url}: {e}")

with open(parsed_urls_file_name,'a') as file:
    for url in new_urls:
        file.write(f"{url}\n")

CronLogFileName = '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/ScrapingCronJob.log'
with open(CronLogFileName, 'a') as file:
    file.write(f"\t\tForbes: {article_count} artículos scraped")

print(f"SUCCESS. Se guardo todo en {csv_file_name}")
