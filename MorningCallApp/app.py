from flask import Flask, render_template
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv
import mysql.connector
import json
import locale

load_dotenv()

app = Flask(__name__)
with open("config.json") as config_file:
    config = json.load(config_file)

@app.route('/')
def home():
    locale.setlocale(locale.LC_TIME, 'es_ES')
    current_date = datetime.now()
    formatted_date = current_date.strftime("%A, %d de %B del %Y").capitalize()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM final_articles ORDER BY rating DESC;");
    articles = cursor.fetchall()

    cursor.close()
    conn.close()

    industry_counts = Counter(article['industry'] for article in articles)
    total_industries_count = sum(industry_counts.values())
    industry_percentages = {industry: (count/total_industries_count) * 100 for industry, count in industry_counts.items()}

    industries = list(industry_percentages.keys())
    industry_percentage = list(industry_percentages.values())

    return render_template('index.html', articles=articles, date=formatted_date, industries=industries, industry_percentage=industry_percentage)

@app.route('/about')
def about():
    return render_template('about.html')

def get_db_connection():
    return mysql.connector.connect(
        host = config["DB_HOST"],
        user = config["DB_USER"],
        password = config["DB_PASS"],
        database = config["DB_NAME"]
    )

if __name__ == '__main__':
    app.run(debug=True)