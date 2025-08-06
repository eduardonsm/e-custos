import sqlite3
from model.Cost import Cost

class CostRepository:
    def __init__(self, db_path="model/LoginSystem.db", conn=None):
        self.db_path = db_path
        self.conn = conn

    def get_connection(self):
        if self.conn:
            return self.conn
        return sqlite3.connect(self.db_path)

    def create_dbCosts(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS costs (
                code INTEGER PRIMARY KEY,
                product INTEGER NOT NULL,
                description TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unitPrice REAL NOT NULL,
                totalPrice REAL NOT NULL,
                is_fixo BOOLEAN NOT NULL,
                is_direto BOOLEAN NOT NULL,
                is_relevante BOOLEAN NOT NULL,
                is_eliminavel BOOLEAN NOT NULL,
                is_oculto BOOLEAN NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product) REFERENCES products (id)
            );
            """)
        conn.commit()
        if self.conn is None:
            conn.close()

    def add_cost(self, cost, user_id):

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO costs 
                        (code, product, description, quantity, unitPrice, totalPrice, is_fixo, is_direto, is_relevante,
                        is_eliminavel, is_oculto, user_id)VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                       (cost.code, cost.product, cost.description, cost.quantity, cost.unitPrice, cost.totalPrice,
                        cost.is_fixo, cost.is_direto, cost.is_relevante, cost.is_eliminavel, cost.is_oculto, user_id))
        conn.commit()
        if self.conn is None:
            conn.close()
        return True
    
    def get_costs_by_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM costs WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        costs = []
        for row in rows:
            cost = Cost(
                code=row[0], product=row[1], description=row[2],
                quantity=row[3], unitPrice=row[4], is_fixo=row[5],
                is_direto=row[5], is_relevante=row[6], is_eliminavel=row[7],
                is_oculto=row[8]
            )
            costs.append(cost)
        if self.conn is None:
            conn.close()
        return costs
    def get_cost_by_code(self,code, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM costs WHERE code = ? AND user_id = ?", (code, user_id))
        row = cursor.fetchone()
        
        if row:
            return Cost(
                code=row[0], product=row[1], description=row[2],
                quantity=row[3], unitPrice=row[4], is_fixo=row[5],
                is_direto=row[5], is_relevante=row[6], is_eliminavel=row[7],
                is_oculto=row[8]
            )
        if self.conn is None:
            conn.close()
        return None
    
    def update_cost(self,code, product, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE costs
            SET product = ?, description = ?, quantity = ?, unitPrice = ?, is_fixo = ?, is_direto = ?, is_relevante = ?, is_eliminavel = ?, is_oculto = ?
            WHERE code = ? AND user_id = ?
        """, (product, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto, code, user_id))
        updated = cursor.rowcount
        conn.commit()
        if self.conn is None:
            conn.close()
        return updated > 0
    def delete_cost(self, code, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM costs WHERE code = ? AND user_id = ?", (code, user_id))
        deleted = cursor.rowcount
        conn.commit()
        if self.conn is None:
            conn.close()
        return deleted > 0