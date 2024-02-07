import os
import sys
import json
import subprocess
import mysql.connector
import pytz

from datetime import datetime

with open('/Users/quevedo/Documents/ITAM/Tesis/MorningCall/VMPipeline/config.json') as f:
    config = json.load(f)
DB_INFO = config['DATABASE_INFO']

articles = json.loads(sys.stdin.read())

print("\n\nATTRIBUTES:")
for article in articles:
    for key, value in article.items():
        print(f"{key}: {value}")
    print()

def get_db_connection():
    return mysql.connector.connect(
        host = DB_INFO["DB_HOST"],
        user = DB_INFO["DB_USER"],
        password = DB_INFO["DB_PASS"],
        database = DB_INFO["DB_NAME"]
    )

def get_current_date_CST():
    central = pytz.timezone('America/Mexico_City')
    now_utc = datetime.now(pytz.utc)
    now_central = now_utc.astimezone(central)
    return now_central.date()

try:
    print("Establishing DB Connection...")
    conn = get_db_connection()
    cursor = conn.cursor()

    for article in articles:
        article_data = (article["fecha"],article["rating"],article["titulo"],article["summary"],article["texto"],article["industry"],get_current_date_CST(),article["source"],article["url"])
        sql_insert_query = """INSERT INTO final_articles (article_date, rating, title, summary, content, industry, date_of_appearance, source, url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql_insert_query, article_data)
        conn.commit()
        print(f"Inserted {article['titulo']} into DB")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Database Connection Error: {e}")