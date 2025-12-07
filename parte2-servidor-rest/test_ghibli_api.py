import requests
import json

BASE_URL = "https://ghibliapi.vercel.app"

print("="*60)
print("TESTANDO API STUDIO GHIBLI")
print("="*60)

# Testar listagem de filmes
print("\n1. LISTANDO FILMES:")
response = requests.get(f"{BASE_URL}/films")
films = response.json()
print(f"Total de filmes: {len(films)}")
print(f"Primeiro filme: {films[0]['title']}")

# Testar listagem de personagens
print("\n2. LISTANDO PERSONAGENS:")
response = requests.get(f"{BASE_URL}/people")
people = response.json()
print(f"Total de personagens: {len(people)}")
print(f"Primeiro personagem: {people[0]['name']}")

# Testar buscar um personagem específico
print("\n3. BUSCANDO PERSONAGEM ESPECÍFICO:")
person_id = people[0]['id']
response = requests.get(f"{BASE_URL}/people/{person_id}")
person = response.json()
print(f"Nome: {person['name']}")
print(f"Gênero: {person['gender']}")
print(f"Idade: {person['age']}")

print("\n" + "="*60)
print("API FUNCIONANDO PERFEITAMENTE!")
print("="*60)
