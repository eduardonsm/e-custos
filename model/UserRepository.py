import sqlite3
from model.User import User
from model.Cost import Cost
class UserRepository:
    def __init__(self, db_path="model/LoginSystem.db"):
        self.db_path = db_path
    def create_dbUsers():
        conn = sqlite3.connect("model/LoginSystem.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            metodo TEXT,
            principio TEXT
        );
        """)
        conn.commit()
        conn.close()
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
    def add_user(self, username, email, password):
        user = User(username, email, password)
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                           (user.nome, user.email, user.password))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    def authenticate_user(self):
            username = self.username_input.text()
            password = self.password_input.text()
            
            conn = sqlite3.connect("model/LoginSystem.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()
            return user
    def have_methods_or_principles(self, user_id):
        conn = sqlite3.connect("model/LoginSystem.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT metodo, principio
            FROM users
            WHERE id = ?
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            metodo, principio = result
            return (metodo is not None and metodo != '') or (principio is not None and principio != '')
        return False
    def update_principio_metodo(self, user_id, metodo, principio):
        conn = sqlite3.connect("model/LoginSystem.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET metodo = ?, principio = ?
            WHERE id = ?
        """, (metodo, principio, user_id))
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