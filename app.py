from flask import Flask, request, jsonify
import sqlite3
import validators
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def init_db():
    try:
        with sqlite3.connect('database.db') as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         titulo TEXT NOT NULL,
                         categoria TEXT NOT NULL,
                         autor TEXT NOT NULL,
                         imagem_url TEXT NOT NULL
                         )""")
            print("Banco de dados criado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar banco de dados: {e}")


init_db()


@app.route('/')
def home_page():
    return "<h2>Minha página com Flask</h2>"


def validar_link_http(url):
    return bool(validators.url(url))


@app.route('/doar', methods=['POST'])
def doar():
    try:
        dados = request.get_json()
        titulo = str(dados.get('titulo', ''))
        categoria = str(dados.get('categoria', ''))
        autor = str(dados.get('autor', ''))
        imagem_url = str(dados.get('imagem_url', ''))
        print(validar_link_http(imagem_url))
        if not all([titulo, categoria, autor, imagem_url]):
            return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

        if validar_link_http(imagem_url) != True:
            return jsonify({"erro": "URL da imagem é inválida"}), 400

        with sqlite3.connect('database.db') as conn:
            conn.execute("""
                INSERT INTO livros (titulo, categoria, autor, imagem_url)
                VALUES (?, ?, ?, ?)
            """, (titulo, categoria, autor, imagem_url))
            conn.commit()

        return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao cadastrar o livro: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
