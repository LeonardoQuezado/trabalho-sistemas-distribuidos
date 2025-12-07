from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'chave-secreta-ghibli'

SERVER_URL = "http://localhost:5000"

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/people')
def people():
    """Lista todos os personagens"""
    try:
        response = requests.get(f"{SERVER_URL}/people")
        personagens = response.json()
        return render_template('people.html', personagens=personagens)
    except Exception as e:
        flash(f"Erro ao buscar personagens: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/person/<person_id>')
def person_detail(person_id):
    """Detalhes de um personagem"""
    try:
        response = requests.get(f"{SERVER_URL}/people/{person_id}")
        personagem = response.json()
        return render_template('person_detail.html', personagem=personagem)
    except Exception as e:
        flash(f"Erro ao buscar personagem: {str(e)}", "error")
        return redirect(url_for('people'))

@app.route('/favorites')
def favorites():
    """Lista favoritos"""
    try:
        response = requests.get(f"{SERVER_URL}/favorites")
        favoritos = response.json()
        return render_template('favorites.html', favoritos=favoritos)
    except Exception as e:
        flash(f"Erro ao buscar favoritos: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/add_favorite/<person_id>', methods=['POST'])
def add_favorite(person_id):
    """Adiciona aos favoritos"""
    try:
        response = requests.post(
            f"{SERVER_URL}/favorites",
            json={"person_id": person_id}
        )
        if response.status_code == 201:
            flash("Personagem adicionado aos favoritos!", "success")
        else:
            flash(response.json().get('error', 'Erro desconhecido'), "error")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
    
    return redirect(url_for('favorites'))

@app.route('/remove_favorite/<person_id>', methods=['POST'])
def remove_favorite(person_id):
    """Remove dos favoritos"""
    try:
        response = requests.delete(f"{SERVER_URL}/favorites/{person_id}")
        if response.status_code == 200:
            flash("Personagem removido dos favoritos!", "success")
        else:
            flash(response.json().get('error', 'Erro desconhecido'), "error")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
    
    return redirect(url_for('favorites'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
