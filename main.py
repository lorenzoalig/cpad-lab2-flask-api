import flask
import requests
import csv
import json

from flask import jsonify

# ========================== COLETA =============================

# Buscando os dados da API (escolhida uma de Naruto)
base_url = "https://dattebayo-api.onrender.com"

# Escolhido quatro collections para buscar na API:
# --------------------------------------------- Personagens
# URL
characters_url = base_url + "/characters"

character_resp = requests.get(characters_url)
characters = character_resp.json()["characters"]

# Abre arquivo e escreve os personagens
with open('naruto_characters.csv', 'w', newline='', encoding='utf-8') as characters_csv:
    headers = characters[0].keys()
    writer = csv.DictWriter(characters_csv, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(characters)

# --------------------------------------------- Vilas
# URL
villages_url = base_url + "/villages"

villages_resp = requests.get(villages_url)
villages = villages_resp.json()["villages"]

# Abre arquivo e escreve as vilas
with open('naruto_villages.csv', 'w', newline='', encoding='utf-8') as villages_csv:
    headers = villages[0].keys()
    writer = csv.DictWriter(villages_csv, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(villages)


# --------------------------------------------- Clans
# URL
clans_url = base_url + "/clans"

clans_resp = requests.get(clans_url)
clans = clans_resp.json()["clans"]

# Abre arquivo e escreve os clans
with open('naruto_clans.csv', 'w', newline='', encoding='utf-8') as clans_csv:
    headers = clans[0].keys()
    writer = csv.DictWriter(clans_csv, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(clans)


# --------------------------------------------- Membros da Akatsuki
# URL
akatsuki_url = base_url + "/akatsuki"

akatsuki_resp = requests.get(akatsuki_url)
akatsuki = akatsuki_resp.json()["akatsuki"]

# Abre arquivo e escreve os membros da Akatsuki
with open('naruto_akatsuki.csv', 'w', newline='', encoding='utf-8') as akatsuki_csv:
    headers = akatsuki[0].keys()
    writer = csv.DictWriter(akatsuki_csv, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(akatsuki)


# ========================== API =============================

app = flask.Flask(__name__)

# Tela inicial
@app.route('/', methods=['GET'])
def home():
    return '<h1>Bem vindo à API de Naruto</h1><br/><h2>Navegue pelos endpoints!</h2>'

# --------------------------------------------- Personagens
@app.route('/personagens', methods=['GET'])
def get_personagens():
    with open('naruto_characters.csv', 'r', newline='', encoding='utf-8') as characters_file:
        reader = csv.DictReader(characters_file)
        return jsonify(list(reader)), 200

@app.route('/personagens/<int:id>', methods=['GET'])
def get_personagem(id):
    with open('naruto_characters.csv', 'r', newline='', encoding='utf-8') as characters_file:
        reader = csv.DictReader(characters_file)

        for char in reader:
            if char.get('id') == str(id):
                return jsonify(char), 200

    return jsonify({"error": "Personagem não encontrado"}), 404

# --------------------------------------------- Vilas
@app.route('/vilas', methods=['GET'])
def get_vilas():
    with open('naruto_villages.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return jsonify(list(reader)), 200


@app.route('/vilas/<int:id>', methods=['GET'])
def get_vila(id):
    with open('naruto_villages.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for vila in reader:
            if vila.get('id') == str(id):
                return jsonify(vila), 200

    return jsonify({"error": "Vila não encontrada"}), 404


# --------------------------------------------- Clans
@app.route('/clans', methods=['GET'])
def get_clas():
    with open('naruto_clans.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return jsonify(list(reader)), 200

@app.route('/clas/<int:id>', methods=['GET'])
def get_cla(id):
    with open('naruto_clans.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for cla in reader:
            if cla.get('id') == str(id):
                return jsonify(cla), 200

    return jsonify({"error": "Clan não encontrado"}), 404

# --------------------------------------------- Akatsuki
@app.route('/akatsuki', methods=['GET'])
def get_akatsuki():
    with open('naruto_akatsuki.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return jsonify(list(reader)), 200

@app.route('/akatsuki/<int:id>', methods=['GET'])
def get_akatsuki_member(id):
    with open('naruto_akatsuki.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for member in reader:
            if member.get('id') == str(id):
                return jsonify(member), 200

    return jsonify({"error": "Membro não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)