import csv
import logging
import requests
from bs4 import BeautifulSoup
from newspaper import Config, Article

urls = ['https://www.eleconomista.com.mx/seccion/empresas',
'https://www.eleconomista.com.mx/seccion/economia',
'https://www.eleconomista.com.mx/seccion/mercados',
'https://www.eleconomista.com.mx/seccion/sectorfinanciero',
'https://www.eleconomista.com.mx/seccion/estados',
'https://www.eleconomista.com.mx/seccion/politica',
'https://www.eleconomista.com.mx/seccion/energia',
'https://www.eleconomista.com.mx/seccion/finanzaspersonales',
'https://www.eleconomista.com.mx/seccion/internacionales',
'https://www.eleconomista.com.mx/capital-humano',
'https://www.eleconomista.com.mx/seccion/tecnologia',
'https://www.eleconomista.com.mx/seccion/estados']

url_stub = 'https://www.eleconomista.com.mx/seccion' # BeautifulSoup jala links relativos, agregamos el stub para hacerlo absoluto
user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

config = Config()
config.browser_user_agent = user_agent_string
headers = {'User-Agent': user_agent_string}

csv_file_name = 'articulos_el_economista.csv'

# Descomenta la siguiente linea si no sabes wtf going on
# logging.basicConfig(level=logging.DEBUG)

with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Titulo', 'URL'])

    article_count = 1
    for url in urls:
        response = requests.get(url, headers=headers)
        html_pagina = response.content

        soup = BeautifulSoup(html_pagina, 'html.parser')
        links_articulos = soup.select('a.jsx-578919967') # Esto solo jala para eleconomista

        for link in links_articulos:
            try:
                relative_url = link.get('href')
                article_url = url_stub + relative_url
                article = Article(article_url, config=config)
                article.download()
                article.parse()

                titulo = article.title

                writer.writerow([titulo, article_url])
                print(f"Article ({article_count}): {titulo} - {article_url}")
                article_count += 1
            except Exception as e:
                print(f"Valio verga {url}: {e}")

print(f"SUCCESS. Se guardo todo en {csv_file_name}")
