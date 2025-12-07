from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import people_pb2

from dicttoxml import dicttoxml

app = Flask(__name__)
CORS(app)

# URL da API externa
GHIBLI_API = "https://ghibliapi.vercel.app"

# Armazenamento em memória (simulando banco de dados)
favoritos = []

# ==================== ROTAS DE PERSONAGENS (CRUD) ====================

@app.route('/people', methods=['GET'])
def get_people():
    """Lista todos os personagens da API Ghibli"""
    formato = request.args.get('format', 'json')
    
    # Consumir API externa
    response = requests.get(f"{GHIBLI_API}/people")
    data = response.json()
    
    # Retornar no formato solicitado
    if formato == 'xml':
        xml_data = dicttoxml(data, custom_root='people', attr_type=False)
        return Response(xml_data, mimetype='application/xml')
    elif formato == 'protobuf':
        # Criar mensagem Protocol Buffer
        people_list = people_pb2.PeopleList()
        
        for person_data in data:
            person = people_list.people.add()
            person.id = person_data.get('id', '')
            person.name = person_data.get('name', '')
            person.gender = person_data.get('gender', '')
            person.age = person_data.get('age', '')
            person.eye_color = person_data.get('eye_color', '')
            person.hair_color = person_data.get('hair_color', '')
            person.species = person_data.get('species', '')
            person.url = person_data.get('url', '')
            
            # Adicionar filmes
            if 'films' in person_data and person_data['films']:
                person.films.extend(person_data['films'])
        
        # Serializar para bytes
        protobuf_data = people_list.SerializeToString()
        return Response(protobuf_data, mimetype='application/x-protobuf')
    else:
        return jsonify(data)
    
@app.route('/people/<person_id>', methods=['GET'])
def get_person(person_id):
    """Busca um personagem específico pelo ID"""
    formato = request.args.get('format', 'json')
    
    # Consumir API externa
    response = requests.get(f"{GHIBLI_API}/people/{person_id}")
    
    if response.status_code == 404:
        return jsonify({"error": "Personagem não encontrado"}), 404
    
    data = response.json()
    
    # Retornar no formato solicitado
    if formato == 'xml':
        xml_data = dicttoxml(data, custom_root='person', attr_type=False)
        return Response(xml_data, mimetype='application/xml')
    else:
        return jsonify(data)

# ==================== ROTAS DE FAVORITOS ====================

@app.route('/favorites', methods=['GET'])
def get_favorites():
    """Lista todos os personagens favoritos"""
    formato = request.args.get('format', 'json')
    
    if formato == 'xml':
        xml_data = dicttoxml(favoritos, custom_root='favorites', attr_type=False)
        return Response(xml_data, mimetype='application/xml')
    else:
        return jsonify(favoritos)

@app.route('/favorites', methods=['POST'])
def add_favorite():
    """Adiciona um personagem aos favoritos"""
    data = request.get_json()
    
    if not data or 'person_id' not in data:
        return jsonify({"error": "person_id é obrigatório"}), 400
    
    person_id = data['person_id']
    
    # Verificar se personagem existe na API
    response = requests.get(f"{GHIBLI_API}/people/{person_id}")
    if response.status_code == 404:
        return jsonify({"error": "Personagem não encontrado"}), 404
    
    person = response.json()
    
    # Verificar se já está nos favoritos
    if any(fav['id'] == person_id for fav in favoritos):
        return jsonify({"error": "Personagem já está nos favoritos"}), 409
    
    # Adicionar aos favoritos
    favorito = {
        "id": person['id'],
        "name": person['name'],
        "gender": person['gender'],
        "age": person['age']
    }
    favoritos.append(favorito)
    
    return jsonify({
        "message": "Personagem adicionado aos favoritos",
        "favorite": favorito
    }), 201

@app.route('/favorites/<person_id>', methods=['DELETE'])
def remove_favorite(person_id):
    """Remove um personagem dos favoritos"""
    global favoritos
    
    # Buscar e remover
    favoritos_filtrados = [fav for fav in favoritos if fav['id'] != person_id]
    
    if len(favoritos_filtrados) == len(favoritos):
        return jsonify({"error": "Personagem não encontrado nos favoritos"}), 404
    
    favoritos = favoritos_filtrados
    
    return jsonify({"message": "Personagem removido dos favoritos"}), 200

# ==================== ROTA RAIZ ====================

@app.route('/')
def index():
    return jsonify({
        "message": "API Studio Ghibli - Sistema de Favoritos",
        "endpoints": {
            "GET /people": "Lista todos os personagens",
            "GET /people/<id>": "Busca personagem por ID",
            "GET /favorites": "Lista favoritos",
            "POST /favorites": "Adiciona favorito",
            "DELETE /favorites/<id>": "Remove favorito"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
