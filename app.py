from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import psycopg2
import json
import os 
from datetime import datetime

# Configuração da conexão com PostgreSQL
DB_HOST = os.getenv("DB_HOST", "dpg-d36lol8gjchc73cemo80-a.oregon-postgres.render.com")
DB_NAME = os.getenv("DB_NAME", "usina_database_mzkw")
DB_USER = os.getenv("DB_USER", "willi")
DB_PASS = os.getenv("DB_PASS", "bqJp74aITRmq6JW4fsQegEHhbBurcZsc")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

# Definição do app
app = FastAPI(title="Usina Solar API", version="2.0.0")

# Modelos Pydantic para validação
class Leitura(BaseModel):
    usina_nome: str
    equipamento_nome: str
    timestamp: datetime  # você pode trocar para datetime se quiser validar formato
    dados: Dict[str, Any]

class Payload(BaseModel):
    leituras: List[Leitura]

@app.get("/")
async def home():
    return {"mensagem": "API da Usina Solar no ar"}

@app.post("/api/receber-leitura")
def receber_leitura(payload: Payload):
    try:
        leituras = payload.leituras
        if not leituras:
            raise HTTPException(status_code=400, detail="Payload vazio")

        conn = get_db_connection()
        cur = conn.cursor()

        for leitura in leituras:
            cur.execute(
                """
                INSERT INTO leituras_remotas (usina_nome, equipamento_nome, timestamp, dados_json)
                VALUES (%s, %s, %s, %s)
                """,
                (leitura.usina_nome, leitura.equipamento_nome, leitura.timestamp, json.dumps(leitura.dados))
            )

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "lote gravado com sucesso"}

    except Exception as e:
        print(f"[ERRO] {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
