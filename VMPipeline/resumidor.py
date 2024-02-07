import os
import sys
import json
import subprocess

from openai import OpenAI

# from config import OPENAI_API_KEY
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

print("Resumiendo...")

with open('/Users/quevedo/Documents/ITAM/Tesis/MorningCall/VMPipeline/config.json') as f:
    config = json.load(f)
openai_api_key = config['OPENAI_API']['key']
OpenAI.api_key = openai_api_key
client = OpenAI()

articles = json.loads(sys.stdin.read())

new_prompt = f"You are an intelligent assistant expert in financial and economic events. Your task is to read financial articles and provide a brief, precise and neutral summary in spanish. The summary should:"\
             "1. Highlight Key Information.\n"\
             "2. Maintain Factual Accuracy.\n"\
             "3. Be Brief (no more than 50 words).\n"\
             "4. Only display the summary, no newline or special characters.\n"\
             "5. Include Important Figures.\n"\
             "6. Mention Key Players.\n"\
             "Remember to maintain neutrality and avoid speculative language."

def resumir_articulo(article, role_option = 2):
    try:
        gpt_roles = [
            "Your task is to provide a concise (20 words max) and accurate summary of news articles in spanish. Focus on the main events, key facts, and essential details. Avoid personal opinions or interpretations, and maintain a neutral tone throughout. Output summary as a JSON with no newline characters.",
            "Provide a brief yet informative summary of news articles in spanish, ensuring you cover the who, what, when, where, why, and how. Keep the summary to a few sentences no more than 25 words and avoid extraneous details. Prioritize accuracy and clarity. Maintain a neutral tone, output the summary as a JSON with no newline characters.",
            new_prompt
        ]
        gpt_prompt = f" Summarize this article: {article['texto']}"
        prompt = gpt_roles[role_option] + gpt_prompt
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            seed=21,
            prompt=prompt,
            temperature=0.3,
            max_tokens=500
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
for article in articles:
    resumen = resumir_articulo(article)
    article["summary"] = resumen.choices[0].text.strip()

subprocess.run(['python3', '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/VMPipeline/db_connection.py'], input=json.dumps(articles), text=True)