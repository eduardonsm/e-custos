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