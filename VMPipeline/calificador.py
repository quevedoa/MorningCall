import os
import sys
import json
import subprocess

from openai import OpenAI
# from config import OPENAI_API_KEY
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
with open('/Users/quevedo/Documents/ITAM/Tesis/MorningCall/VMPipeline/config.json') as f:
    config = json.load(f)
openai_api_key = config['OPENAI_API']['key']
OpenAI.api_key = openai_api_key
client = OpenAI()

print("Calificando...")

articles = json.loads(sys.stdin.read())

# articles_csv_path = './articulos.csv'
# articles = []
# with open(articles_csv_path, 'r', newline='') as csvfile:
#     csv_reader = csv.DictReader(csvfile)
#     for row in csv_reader:
#         article = {
#             "title": row['title'],
#             "date": row['date'],
#             "content": row['content']
#         }
#         articles.append(article)

# old_ranking_role = f"""Your role is to act as an Article Ranking Assistant. You will be provided with financial articles, each containing title, date, and content. Your task is to rate these articles based on the following criteria (each on a scale from 1 to 10):
#             Scale: How many people the event affected?
#             Magnitude: How big was the effect?
#             Potential: How likely it is that the event will cause bigger events?
#             Immediacy: How close in time is the event?
#             Significance: How much the event affects the financial market as a whole? 
#             For each article, only provide a total score out of 50 nothing more in JSON format, derived from the individual ratings for each criterion. Your evaluation will help in prioritizing these articles for readers who seek the most relevant and insightful financial news.""",

# Sector Relevance: how relevant is to the {sector_financiero} sector
ranking_role = f"""Your role is to act as an Article Ranking Assistant for mexican investors. You will be provided with financial articles, each containing title, date, and content. Your task is to rate these articles based on the following criteria:
            Local Market Impact: How significant is it to the Mexican financial market in the near future?
            Economy: How significant is it to key economic indicators of Mexico?
            Politics: How significant is it to the political climate of Mexico?
            Prices: How impactful is it to the change in price of a financial instrument?
            Risk: How much risk does it imply for financial investors?
            Magnitude: If the event is international, how big and significant is it?
            Timeliness: How outdated is the article?
            Respond to me by ONLY provide a JSON containing a score from 0 to 10 derived from the individual ratings for each criterion."""

def ranking_prompt(article):
    return f"""Analyze this article and return the scores in JSON:
        Title: {article['titulo']}
        Date: {article['fecha']}
        Content: {article['texto']}"""

def rank_article(article, sector_financiero=""):
    try:
        gpt_role = ranking_role
        gpt_prompt = ranking_prompt(article)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            seed=21,
            temperature=0.3,
            messages=[
                {"role": "system", "content": gpt_role},
                {"role": "user", "content": gpt_prompt}
            ]
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

client = OpenAI()

# ELIMINAR ARTICULOS ANALIZADOS SOLO ES PARA QUE NO SE PASE DE 5 ARTICULOS DURANTE TESTING
articulos_analizados = []
for i in range(10 if len(articles) >= 10 else len(articles)):
    articulos_analizados.append(articles[i])

calificaciones_test = []
for article in articulos_analizados:
    calificaciones_test.append(rank_article(article))

for i, response in enumerate(calificaciones_test):
    contenido = response.choices[0].message.content
    calificaciones = json.loads(contenido)
    print(f"{articulos_analizados[i]['titulo']}")

    total = 0
    sum = 0
    for key, val in calificaciones.items():
        print(f"Criterio: {key}, Calif: {val}")
        total += 1
        sum += int(val)
    prom = sum / total
    print(f"Promedio: {prom}")
    articulos_analizados[i]["rating"] = round(prom, 2)

subprocess.run(['python3', '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/VMPipeline/resumidor.py'], input=json.dumps(articulos_analizados), text=True)

