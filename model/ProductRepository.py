import sqlite3
from model.Product import Product

class ProductRepository:
    def __init__(self, db_path="model/LoginSystem.db", conn=None):
        self.db_path = db_path
        self.conn = conn

    def get_connection(self):
        if self.conn:
            return self.conn
        return sqlite3.connect(self.db_path)

    def create_dbProducts(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                unit TEXT NOT NULL,
                category TEXT NOT NULL CHECK(category IN ('Acabado', 'Semiacabado', 'Componente', 'Matéria-prima')),
                status TEXT NOT NULL CHECK(status IN ('Ativo', 'Inativo', 'Em desenvolvimento')),
                production_centers INTEGER NOT NULL,
                production_flow TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
        if self.conn is None:
            conn.close()

    def add_product(self, product):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (description, unit, category, status, production_centers, production_flow, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product.description,
            product.unit,
            product.category,
            product.status,
            product.production_centers,
            product.production_flow,
            product.user_id
        ))
        product.id = cursor.lastrowid
        conn.commit()
        if self.conn is None:
            conn.close()
        return True

    def get_products_by_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE user_id = ? ORDER BY description", (user_id,))
        rows = cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(
                product_id=row[0],
                description=row[1],
                unit=row[2],
                category=row[3],
                status=row[4],
                production_centers=row[5],
                production_flow=row[6],
                user_id=row[7]
            ))
        if self.conn is None:
            conn.close()
        return products

    def get_product_by_id(self, product_id, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ? AND user_id = ?", (product_id, user_id))
        row = cursor.fetchone()
        
        if row:
            product = Product(
                product_id=row[0],
                description=row[1],
                unit=row[2],
                category=row[3],
                status=row[4],
                production_centers=row[5],
                production_flow=row[6],
                user_id=row[7]
            )
            if self.conn is None:
                conn.close()
            return product
        if self.conn is None:
            conn.close()
        return None

    def update_product(self, product):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET description = ?,
                unit = ?,
                category = ?,
                status = ?,
                production_centers = ?,
                production_flow = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        """, (
            product.description,
            product.unit,
            product.category,
            product.status,
            product.production_centers,
            product.production_flow,
            product.id,
            product.user_id
        ))
        updated = cursor.rowcount
        conn.commit()
        if self.conn is None:
            conn.close()
        return updated > 0

    def delete_product(self, product_id, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ? AND user_id = ?", (product_id, user_id))
        deleted = cursor.rowcount
        conn.commit()
        if self.conn is None:
            conn.close()
        return deleted > 0

    def search_products(self, search_term, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM products 
            WHERE description LIKE ? AND user_id = ?
            ORDER BY description
        """, (f'%{search_term}%', user_id))
        rows = cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(
                product_id=row[0],
                description=row[1],
                unit=row[2],
                category=row[3],
                status=row[4],
                production_centers=row[5],
                production_flow=row[6],
                user_id=row[7]
            ))
        if self.conn is None:
            conn.close()
        return products