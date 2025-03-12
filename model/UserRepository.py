import sqlite3
from model.User import User

class UserRepository:
    def __init__(self, db_path="model/LoginSystem.db"):
        self.db_path = db_path
    
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