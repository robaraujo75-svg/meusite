from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # habilita CORS

# Criar banco de dados e tabela (se não existir)
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inscricoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                email TEXT,
                telefone TEXT,
                origem TEXT,
                estado TEXT,
                cidade TEXT,
                nascimento TEXT,
                plano TEXT,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

init_db()

# Rota para receber inscrições
@app.route("/inscrever", methods=["POST"])
def inscrever():
    data = request.get_json()

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inscricoes (nome, email, telefone, origem, estado, cidade, nascimento, plano)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("fullName"),
            data.get("email"),
            data.get("phone"),
            data.get("source"),
            data.get("state"),
            data.get("city"),
            data.get("birthDate"),
            data.get("plan")
        ))
        conn.commit()

    return jsonify({"status": "success"}), 200

# Rota para listar inscrições
@app.route("/inscricoes", methods=["GET"])
def listar():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inscricoes ORDER BY data_registro DESC")
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
