import sqlite3

DB = 'servidor_leituras.db'

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS leituras_remotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usina_nome TEXT NOT NULL,
    equipamento_nome TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    dados_json TEXT NOT NULL,
    recebido_em DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print("[INFO] Banco de dados criado com sucesso.")
