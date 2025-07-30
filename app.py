from flask import Flask, request, jsonify
import psycopg2
import json 
import os
from datetime import datetime

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return {"mensagem": "API da Usina Solar no ar"}

# Configuração da conexão com PostgreSQL (exemplo: Render)
DB_HOST = os.getenv("DB_HOST", "dpg-d24jgfidbo4c73eck56g-a.oregon-postgres.render.com")
DB_NAME = os.getenv("DB_NAME", "usina_database")
DB_USER = os.getenv("DB_USER", "willi")
DB_PASS = os.getenv("DB_PASS", "Oi79dL1qcBsAH69xBGNqALU3xFwFWcwj")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

@app.route('/api/receber-leitura', methods=['POST'])
def receber_leitura():
    try:
        data = request.get_json()
        leituras = data.get("leituras", [])

        if not leituras: 
            return jsonify({"erro": "Payload vazio"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()

        for leitura in leituras: 
            usina = leitura.get('usina_nome')
            equipamento = leitura.get('equipamento_nome')
            timestamp = leitura.get('timestamp')
            dados = json.dumps(leitura.get("dados", {}))

            cur.execute('''
                INSERT INTO leituras_remotas (usina_nome, equipamento_nome, timestamp, dados_json)
                VALUES (%s, %s, %s, %s)
            ''', (usina, equipamento, timestamp, dados))

        conn.commit() 
        cur.close() 
        conn.close()
        return jsonify({"status": "lote gravado com sucesso"}), 200

    except Exception as e:
        print(f"[ERRO] {e}")
        return jsonify({"erro": f"Erro interno: {e}"}), 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
