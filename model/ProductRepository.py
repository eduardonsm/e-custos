import sqlite3
from model.Product import Product
import json

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
                name TEXT NOT NULL,
                dateProject TEXT,
                dateStart TEXT,
                isActive INTEGER NOT NULL,
                endTime TEXT,
                price REAL,
                productTree TEXT, -- usamos TEXT no SQLite para armazenar JSON
                user_id INTEGER NOT NULL
            );
        """)
        conn.commit()
        if self.conn is None:
            conn.close()

    def add_product(self, product, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, dateProject, dateStart, isActive, endTime, price, productTree, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product.name, product.dateProject, product.dateStart,
            int(product.isActive), product.endTime, product.price,
            product.productTree, user_id
        ))
        conn.commit()
        if self.conn is None:
            conn.close()
        return True

    def get_products_by_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        products = []
        for row in rows:
            product = Product(row[1], row[2], row[3], bool(row[4]), row[5], row[6], row[7])
            products.append(product)
        if self.conn is None:
            conn.close()
        return products

    def get_product_by_id(self, product_id, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ? AND user_id = ?", (product_id, user_id))
        row = cursor.fetchone()
        
        if row:
            return Product(row[1], row[2], row[3], bool(row[4]), row[5], row[6], row[7])
        if self.conn is None:
            conn.close()
        return None

    def update_product(self, product_id, user_id, name, dateProject, dateStart, isActive, endTime, price, productTree):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET name = ?, dateProject = ?, dateStart = ?, isActive = ?, endTime = ?, price = ?, productTree = ?
            WHERE id = ? AND user_id = ?
        """, (name, dateProject, dateStart, int(isActive), endTime, price, productTree, product_id, user_id))
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
