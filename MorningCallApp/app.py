from flask import Flask, render_template
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv
import mysql.connector
import json
import locale
import colorsys
import pytz

load_dotenv()

app = Flask(__name__)
with open("config.json") as config_file:
    config = json.load(config_file)

@app.route('/')
def home():
    locale.setlocale(locale.LC_TIME, 'es_ES')
    current_date = datetime.now()
    formatted_date = current_date.strftime("%A, %d de %B del %Y").capitalize()

    #  WHERE date_of_appearance = {get_current_date_CST()}
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM final_articles WHERE date_of_appearance = "{get_current_date_CST()}" ORDER BY rating DESC;');
    articles = cursor.fetchall()

    cursor.close()
    conn.close()

    industry_counts = Counter(article['industry'] for article in articles)
    total_industries_count = sum(industry_counts.values())
    industry_percentages = {industry: (count/total_industries_count) * 100 for industry, count in industry_counts.items()}

    industries = list(industry_percentages.keys())
    industry_percentage = list(industry_percentages.values())
    pie_chart_colors = get_unique_colors(len(industries))

    return render_template('index.html', 
                           articles=articles, 
                           date=formatted_date, 
                           industries=industries, 
                           industry_percentage=industry_percentage, 
                           pie_chart_colors=pie_chart_colors)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def get_db_connection():
    return mysql.connector.connect(
        host = config["DB_HOST"],
        user = config["DB_USER"],
        password = config["DB_PASS"],
        database = config["DB_NAME"]
    )

def get_unique_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        lightness = 0.5
        saturation = 0.8
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append('#' + ''.join(f'{int(x*255):02x}' for x in rgb))

def get_current_date_CST():
    central = pytz.timezone('America/Mexico_City')
    now_utc = datetime.now(pytz.utc)
    now_central = now_utc.astimezone(central)
    return now_central.date()
    

if __name__ == '__main__':
    app.run(debug=True)