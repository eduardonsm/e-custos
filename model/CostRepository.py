import sqlite3
from model.Cost import Cost
class CostRepository:
    def __init__(self, db_path="model/LoginSystem.db"):
        self.db_path = db_path
    
    def create_dbCosts():
        conn = sqlite3.connect("model/LoginSystem.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS costs (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT NOT NULL,
                is_direto BOOLEAN NOT NULL,  
                is_fixo BOOLEAN NOT NULL,
                is_relevante BOOLEAN NOT NULL,
                is_eliminavel BOOLEAN NOT NULL,
                is_oculto BOOLEAN NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
                       );
            """)
        conn.commit()
        conn.close()
    
    def add_cost(cost, user_id):
        nome = cost.nome
        valor = cost.valor
        categoria = cost.categoria
        is_direto = cost.is_direto
        is_fixo = cost.is_fixo
        is_relevante = cost.is_relevante
        is_eliminavel = cost.is_eliminavel
        is_oculto = cost.is_oculto
        
        conn = sqlite3.connect("model/LoginSystem.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO costs (nome, valor, categoria, is_direto, is_fixo, is_relevante, is_eliminavel,is_oculto,user_id) VALUES (?,?,?,?,?,?,?,?,?)",(nome, valor, categoria, is_direto, is_fixo, is_relevante, is_eliminavel, is_oculto, user_id))
        conn.commit()
        conn.close()
        return True