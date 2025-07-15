from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)
DB = 'servidor_leituras.db'

@app.route('/api/receber-leitura', methods=['POST'])
def receber_leitura():
    try:
        data = request.get_json()

        usina = data.get('usina_nome')
        equipamento = data.get('equipamento_nome')
        timestamp = data.get('timestamp')
        dados = data.get('dados')

        if not usina or not equipamento or not timestamp or not dados:
            return jsonify({'erro': 'Campos obrigatórios: usina_nome, equipamento_nome, timestamp, dados'}), 400

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO leituras_remotas (usina_nome, equipamento_nome, timestamp, dados_json)
            VALUES (?, ?, ?, ?)
        ''', (usina, equipamento, timestamp, json.dumps(dados)))
        conn.commit()
        conn.close()

        return jsonify({'status': 'sucesso'}), 200

    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
