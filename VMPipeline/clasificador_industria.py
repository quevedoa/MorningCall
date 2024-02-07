import sys
import json
import random
import subprocess

print("Classifying...")

articulos = json.loads(sys.stdin.read())

industrias = ["Economia","Energia","Materiales","Industrial","Salud","Bienes Raices"]

for articulo in articulos:
    articulo["industry"] = random.choice(industrias)

subprocess.run(['python3', '/Users/quevedo/Documents/ITAM/Tesis/MorningCall/VMPipeline/calificador.py'], input=json.dumps(articulos), text=True)