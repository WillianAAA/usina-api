from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return {"mensagem": "API da Usina Solar no ar"}

DB = 'servidor_leituras.db'

@app.route('/api/receber-leitura', methods=['POST'])
def receber_leitura():
    try:
        data = request.get_json()
        leituras = data.get("leituras", [])

        if not leituras: 
            return jsonify({"erro": "Payload vazio"}), 400
        
        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        for leitura in leituras: 
            usina = leitura.get('usina_nome')
            equipamento = leitura.get('equipamento_nome')
            timestamp = leitura.get('timestamp')
            dados = json.dumps(leitura.get("dados", {}))

            cur.execute('''
                INSERT INTO leituras_remotas (usina_nome, equipamento_nome, timestamp, dados_json)
                VALUES (?, ?, ?, ?)
            ''', (usina, equipamento, timestamp, dados))

        conn.commit()
        conn.close()
        return jsonify({"status": "lote gravado com sucesso"}), 200

    except Exception as e:
        print(f"[ERRO] {e}")
        return jsonify({"erro": f"Erro interno: {e}"}), 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
