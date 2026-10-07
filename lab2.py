import flask
import requests
import csv
import json
import os  # Usado para verificar se o arquivo já existe
import ast  #  Usado para converter os campos salvos como texto em estruturas Python

from flask import jsonify

# Etapa 1 consumo API
# Verificação de arquivo existente 
# Verificação de falhas na API de consumo
# ##

# ========================== COLETA =============================

# Buscando os dados da API (escolhida uma de Naruto)
base_url = "https://dattebayo-api.onrender.com"

# Escolhido quatro collections para buscar na API:
# --------------------------------------------- Personagens
# URL
characters_url = base_url + "/characters"

# Só realiza a coleta se o arquivo ainda não existir
if not os.path.exists('naruto_characters.csv'):
    try:
        character_resp = requests.get(characters_url, timeout=10)
        character_resp.raise_for_status()
        characters = character_resp.json()["characters"]

        # Abre arquivo e escreve os personagens
        with open('naruto_characters.csv', 'w', newline='', encoding='utf-8') as characters_csv:
            headers = characters[0].keys()
            writer = csv.DictWriter(characters_csv, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(characters)

    except requests.RequestException as erro:
        # Trata falha na comunicação com a API externa
        print(f"Erro ao coletar personagens: {erro}")
        raise SystemExit

else:
    print(f"Arquivo naruto_characters.csv já existe.")


# --------------------------------------------- Vilas
# URL
villages_url = base_url + "/villages"

# Só realiza a coleta se o arquivo ainda não existir
if not os.path.exists('naruto_villages.csv'):
    try:
        villages_resp = requests.get(villages_url, timeout=10)
        villages_resp.raise_for_status()
        villages = villages_resp.json()["villages"]

        # Abre arquivo e escreve as vilas
        with open('naruto_villages.csv', 'w', newline='', encoding='utf-8') as villages_csv:
            headers = villages[0].keys()
            writer = csv.DictWriter(villages_csv, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(villages)

    except requests.RequestException as erro:
        # Trata falha na comunicação com a API externa
        print(f"Erro ao coletar vilas: {erro}")
        raise SystemExit
else:
    print(f"Arquivo naruto_villages.csv já existe.")

# --------------------------------------------- Clans
# URL
clans_url = base_url + "/clans"

# Só realiza a coleta se o arquivo ainda não existir
if not os.path.exists('naruto_clans.csv'):
    try:
        clans_resp = requests.get(clans_url, timeout=10)
        clans_resp.raise_for_status()
        clans = clans_resp.json()["clans"]

        # Abre arquivo e escreve os clans
        with open('naruto_clans.csv', 'w', newline='', encoding='utf-8') as clans_csv:
            headers = clans[0].keys()
            writer = csv.DictWriter(clans_csv, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(clans)

    except requests.RequestException as erro:
        # Trata falha na comunicação com a API externa
        print(f"Erro ao coletar clans: {erro}")
        raise SystemExit
else:
    print(f"Arquivo naruto_clans.csv já existe.")

# --------------------------------------------- Membros da Akatsuki
# URL
akatsuki_url = base_url + "/akatsuki"

# Só realiza a coleta se o arquivo ainda não existir
if not os.path.exists('naruto_akatsuki.csv'):
    try:
        akatsuki_resp = requests.get(akatsuki_url, timeout=10)
        akatsuki_resp.raise_for_status()
        akatsuki = akatsuki_resp.json()["akatsuki"]

        # Abre arquivo e escreve os membros da Akatsuki
        with open('naruto_akatsuki.csv', 'w', newline='', encoding='utf-8') as akatsuki_csv:
            headers = akatsuki[0].keys()
            writer = csv.DictWriter(akatsuki_csv, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(akatsuki)

    except requests.RequestException as erro:
        # Trata falha na comunicação com a API externa
        print(f"Erro ao coletar membros da Akatsuki: {erro}")
        raise SystemExit
else:
    print(f"Arquivo naruto_akatsuki.csv já existe.")

# ========================== API =============================

app = flask.Flask(__name__)

# Funções auxiliares para alterar os arquivos CSV
def adicionar_registro(nome_arquivo, dados):
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        registros = list(reader)
        headers = reader.fieldnames

    # Cria um novo ID a partir do maior ID existente
    ids = [int(registro['id']) for registro in registros if registro.get('id', '').isdigit()]
    novo_id = max(ids, default=0) + 1

    dados['id'] = str(novo_id)

    # Mantém somente os campos existentes no CSV
    novo_registro = {}
    for campo in headers:
        novo_registro[campo] = dados.get(campo, '')

    registros.append(novo_registro)

    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(registros)

    return novo_registro


def atualizar_registro(nome_arquivo, id, dados):
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        registros = list(reader)
        headers = reader.fieldnames

    registro_encontrado = None

    for registro in registros:
        if registro.get('id') == str(id):

            # Atualiza somente os campos enviados
            for campo in headers:
                if campo != 'id' and campo in dados:
                    registro[campo] = dados[campo]

            registro_encontrado = registro
            break

    if registro_encontrado is None:
        return None

    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(registros)

    return registro_encontrado


def remover_registro(nome_arquivo, id):
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        registros = list(reader)
        headers = reader.fieldnames

    registro_encontrado = None

    for registro in registros:
        if registro.get('id') == str(id):
            registro_encontrado = registro
            break

    if registro_encontrado is None:
        return None

    registros.remove(registro_encontrado)

    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(registros)

    return registro_encontrado


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


# CREATE - cria um personagem no arquivo local
@app.route('/personagens', methods=['POST'])
def create_personagem():
    dados = flask.request.get_json()

    if not dados:
        return jsonify({"error": "Dados não informados"}), 400

    personagem = adicionar_registro('naruto_characters.csv', dados)

    return jsonify(personagem), 201


# UPDATE - altera um personagem no arquivo local
@app.route('/personagens/<int:id>', methods=['PUT'])
def update_personagem(id):
    dados = flask.request.get_json()

    if not dados:
        return jsonify({"error": "Dados não informados"}), 400

    personagem = atualizar_registro(
        'naruto_characters.csv',
        id,
        dados
    )

    if personagem is None:
        return jsonify({"error": "Personagem não encontrado"}), 404

    return jsonify(personagem), 200


#  DELETE - remove um personagem do arquivo local
@app.route('/personagens/<int:id>', methods=['DELETE'])
def delete_personagem(id):
    personagem = remover_registro(
        'naruto_characters.csv',
        id
    )

    if personagem is None:
        return jsonify({"error": "Personagem não encontrado"}), 404

    return jsonify({"message": "Personagem removido com sucesso"}), 200


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


#  CREATE
@app.route('/vilas', methods=['POST'])
def create_vila():
    dados = flask.request.get_json()

    if not dados:
        return jsonify({"error": "Dados não informados"}), 400

    vila = adicionar_registro('naruto_villages.csv', dados)

    return jsonify(vila), 201


# UPDATE
@app.route('/vilas/<int:id>', methods=['PUT'])
def update_vila(id):
    dados = flask.request.get_json()

    if not dados:
        return jsonify({"error": "Dados não informados"}), 400

    vila = atualizar_registro(
        'naruto_villages.csv',
        id,
        dados
    )

    if vila is None:
        return jsonify({"error": "Vila não encontrada"}), 404

    return jsonify(vila), 200


# DELETE
@app.route('/vilas/<int:id>', methods=['DELETE'])
def delete_vila(id):
    vila = remover_registro(
        'naruto_villages.csv',
        id
    )

    if vila is None:
        return jsonify({"error": "Vila não encontrada"}), 404

    return jsonify({"message": "Vila removida com sucesso"}), 200


# --------------------------------------------- Clans

@app.route('/clans', methods=['GET'])
def get_clas():
    with open('naruto_clans.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return jsonify(list(reader)), 200


# Corrigido /clas para /clans para manter o recurso consistente
@app.route('/clans/<int:id>', methods=['GET'])
def get_cla(id):
    with open('naruto_clans.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for cla in reader:
            if cla.get('id') == str(id):
                return jsonify(cla), 200

    return jsonify({"error": "Clan não encontrado"}), 404


# CREATE
@app.route('/clans', methods=['POST'])
def create_cla():
    dados = flask.request.get_json()

    if not dados:
        return jsonify({"error": "Dados não informados"}), 400

    cla = adicionar_registro('naruto_clans.csv', dados)

    return jsonify(cla), 201


# UPDATE
@app.route('/clans/<int:id>', methods=['PUT'])
def update_cla(id):
    dados = flask.request.get_json()

    if not dados:
        return jsonify({"error": "Dados não informados"}), 400

    cla = atualizar_registro(
        'naruto_clans.csv',
        id,
        dados
    )

    if cla is None:
        return jsonify({"error": "Clan não encontrado"}), 404

    return jsonify(cla), 200


# DELETE
@app.route('/clans/<int:id>', methods=['DELETE'])
def delete_cla(id):
    cla = remover_registro(
        'naruto_clans.csv',
        id
    )

    if cla is None:
        return jsonify({"error": "Clan não encontrado"}), 404

    return jsonify({"message": "Clan removido com sucesso"}), 200


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


# CREATE
@app.route('/akatsuki', methods=['POST'])
def create_akatsuki_member():
    dados = flask.request.get_json()

    if not dados:
        return jsonify({"error": "Dados não informados"}), 400

    member = adicionar_registro('naruto_akatsuki.csv', dados)

    return jsonify(member), 201


# UPDATE
@app.route('/akatsuki/<int:id>', methods=['PUT'])
def update_akatsuki_member(id):
    dados = flask.request.get_json()

    if not dados:
        return jsonify({"error": "Dados não informados"}), 400

    member = atualizar_registro(
        'naruto_akatsuki.csv',
        id,
        dados
    )

    if member is None:
        return jsonify({"error": "Membro não encontrado"}), 404

    return jsonify(member), 200


# DELETE
@app.route('/akatsuki/<int:id>', methods=['DELETE'])
def delete_akatsuki_member(id):
    member = remover_registro(
        'naruto_akatsuki.csv',
        id
    )

    if member is None:
        return jsonify({"error": "Membro não encontrado"}), 404

    return jsonify({"message": "Membro removido com sucesso"}), 200


# ========================== ENDPOINTS COM FILTRO =============================

# --------------------------------------------- Filtros de Personagens
#  Filtra personagens pelo nome do clan
@app.route('/personagens/clan', methods=['GET'])
def get_personagens_por_clan():
    nome_clan = flask.request.args.get('nome')

    # Trata parâmetro ausente ou vazio
    if not nome_clan or not nome_clan.strip():
        return jsonify({"error": "Parâmetro 'nome' do clan é obrigatório"}), 400

    personagens_encontrados = []

    with open('naruto_characters.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for personagem in reader:
            try:
                personal = ast.literal_eval(personagem.get('personal', '{}'))

                clan = personal.get('clan', [])

                # Alguns personagens possuem um clan e outros possuem uma lista de clans
                if isinstance(clan, str):
                    clan = [clan]

                for nome in clan:
                    if nome.lower() == nome_clan.strip().lower():
                        personagens_encontrados.append(personagem)
                        break

            except (ValueError, SyntaxError):
                continue

    if not personagens_encontrados:
        return jsonify({"error": "Nenhum personagem encontrado para este clan"}), 404

    return jsonify(personagens_encontrados), 200


# Filtra personagens pelo nome do jutsu
@app.route('/personagens/jutsu', methods=['GET'])
def get_personagens_por_jutsu():
    nome_jutsu = flask.request.args.get('nome')

    # Trata parâmetro ausente ou vazio
    if not nome_jutsu or not nome_jutsu.strip():
        return jsonify({"error": "Parâmetro 'nome' do jutsu é obrigatório"}), 400

    personagens_encontrados = []

    with open('naruto_characters.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for personagem in reader:
            try:
                jutsus = ast.literal_eval(personagem.get('jutsu', '[]'))

                for jutsu in jutsus:
                    if jutsu.lower() == nome_jutsu.strip().lower():
                        personagens_encontrados.append(personagem)
                        break

            except (ValueError, SyntaxError):
                continue

    if not personagens_encontrados:
        return jsonify({"error": "Nenhum personagem encontrado com este jutsu"}), 404

    return jsonify(personagens_encontrados), 200


if __name__ == '__main__':
    app.run(debug=True)
