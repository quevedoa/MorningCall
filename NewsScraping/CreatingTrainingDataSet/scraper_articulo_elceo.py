import csv
import logging
import requests
from bs4 import BeautifulSoup
from newspaper import Config, Article
import re

urls = ['https://elceo.com/negocios/',
'https://elceo.com/mercados/',
'https://elceo.com/economia/']

url_stub = 'https://www.eleconomista.com.mx/seccion' # BeautifulSoup jala links relativos, agregamos el stub para hacerlo absoluto
user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' # Si no los robots.txt se vuelven locos

config = Config()
config.browser_user_agent = user_agent_string
headers = {'User-Agent': user_agent_string}

# csv_file_name = 'articulos.csv'
csv_file_name = '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/CSVDeArticulos/articulos_elceo.csv'
parsed_urls_file_name = '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/parsed_urls.txt'

# Descomenta la siguiente linea si no sabes wtf going on
# logging.basicConfig(level=logging.DEBUG)

# Checa todos los urls que ya leyó
link_set = set()
with open(parsed_urls_file_name,'r') as file:
    for line in file:
        url = line.strip()
        if url:
            link_set.add(url)

article_count = 0
with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    new_urls = []
    for url in urls:
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

                    writer.writerow([titulo, fecha, texto, article_url])
                    article_count += 1
                    print(f"Article ({article_count}): {titulo} - {article_url}")
            except Exception as e:
                print(f"Valio verga {url}: {e}")

with open(parsed_urls_file_name,'a') as file:
    for url in new_urls:
        file.write(f"{url}\n")

CronLogFileName = '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/ScrapingCronJob.log'
with open(CronLogFileName, 'a') as file:
    file.write(f"\t\tEl CEO: {article_count} artículos scraped")

print(f"SUCCESS. Se guardo todo en {csv_file_name}")
