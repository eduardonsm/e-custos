import sqlite3
from model.ItemCusto import ItemCusto

class ItemCustoRepository:
    def __init__(self, db_path="model/LoginSystem.db", conn=None):
        self.db_path = db_path
        self.conn = conn

    def get_connection(self):
        if self.conn:
            return self.conn
        return sqlite3.connect(self.db_path)

    def create_dbItensCusto(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_custo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id TEXT NOT NULL,
                quantidade REAL NOT NULL,
                medida TEXT NOT NULL CHECK(medida IN ('Unid', 'ml', 'litros', 'kg', 'kW/h', 'h')),
                descricao TEXT NOT NULL,
                valor_unitario REAL NOT NULL,
                valor_total REAL NOT NULL,
                categoria TEXT NOT NULL CHECK(categoria IN ('MD', 'MOD', 'CIF', 'CO')),
                classificacao TEXT NOT NULL CHECK(classificacao IN ('Variável', 'Fixo')),
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
        if self.conn is None:
            conn.close()
    def get_distinct_produto_ids(self, user_id: int) -> list[str]:
        """Retorna uma lista de todos os produto_id únicos para um usuário."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT produto_id FROM itens_custo 
            WHERE user_id = ? 
            ORDER BY produto_id
        """, (user_id,))
        rows = cursor.fetchall()
        if self.conn is None:
            conn.close()
        return [row[0] for row in rows]
    def add_item_custo(self, item: ItemCusto) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO itens_custo 
            (produto_id, quantidade, medida, descricao, valor_unitario, valor_total, categoria, classificacao, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.produto_id,
            item.quantidade,
            item.medida,
            item.descricao,
            item.valor_unitario,
            item.valor_total,
            item.categoria,
            item.classificacao,
            item.user_id
        ))
        item_id = cursor.lastrowid
        conn.commit()
        if self.conn is None:
            conn.close()
        return item_id

    def get_item_custo(self, item_id: int, user_id: int) -> ItemCusto:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM itens_custo 
            WHERE id = ? AND user_id = ?
        """, (item_id, user_id))
        row = cursor.fetchone()
        
        if row:
            item = ItemCusto(
                item_id=row[0],
                produto_id=row[1],
                quantidade=row[2],
                medida=row[3],
                descricao=row[4],
                valor_unitario=row[5],
                valor_total=row[6],
                categoria=row[7],
                classificacao=row[8],
                user_id=row[9]
            )
            if self.conn is None:
                conn.close()
            return item
        if self.conn is None:
            conn.close()
        return None

    def get_itens_by_user(self, user_id: int) -> list[ItemCusto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM itens_custo 
            WHERE user_id = ? 
            ORDER BY produto_id, categoria, descricao
        """, (user_id,))
        rows = cursor.fetchall()
        itens = []
        for row in rows:
            itens.append(ItemCusto(
                item_id=row[0],
                produto_id=row[1],
                quantidade=row[2],
                medida=row[3],
                descricao=row[4],
                valor_unitario=row[5],
                valor_total=row[6],
                categoria=row[7],
                classificacao=row[8],
                user_id=row[9]
            ))
        if self.conn is None:
            conn.close()
        return itens

    def update_item_custo(self, item: ItemCusto) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE itens_custo 
            SET produto_id = ?,
                quantidade = ?,
                medida = ?,
                descricao = ?,
                valor_unitario = ?,
                valor_total = ?,
                categoria = ?,
                classificacao = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        """, (
            item.produto_id,
            item.quantidade,
            item.medida,
            item.descricao,
            item.valor_unitario,
            item.valor_total,
            item.categoria,
            item.classificacao,
            item.id,
            item.user_id
        ))
        updated = cursor.rowcount > 0
        conn.commit()
        if self.conn is None:
            conn.close()
        return updated

    def delete_item_custo(self, item_id: int, user_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM itens_custo 
            WHERE id = ? AND user_id = ?
        """, (item_id, user_id))
        deleted = cursor.rowcount > 0
        conn.commit()
        if self.conn is None:
            conn.close()
        return deleted

    def search_itens(self, search_term: str, user_id: int) -> list[ItemCusto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM itens_custo 
            WHERE (produto_id LIKE ? OR descricao LIKE ?) 
            AND user_id = ?
            ORDER BY produto_id, descricao
        """, (f'%{search_term}%', f'%{search_term}%', user_id))
        rows = cursor.fetchall()
        itens = []
        for row in rows:
            itens.append(ItemCusto(
                item_id=row[0],
                produto_id=row[1],
                quantidade=row[2],
                medida=row[3],
                descricao=row[4],
                valor_unitario=row[5],
                valor_total=row[6],
                categoria=row[7],
                classificacao=row[8],
                user_id=row[9]
            ))
        if self.conn is None:
            conn.close()
        return itens

    def get_itens_by_produto(self, produto_id: str, user_id: int) -> list[ItemCusto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM itens_custo 
            WHERE produto_id = ? AND user_id = ?
            ORDER BY categoria, descricao
        """, (produto_id, user_id))
        rows = cursor.fetchall()
        itens = []
        for row in rows:
            itens.append(ItemCusto(
                item_id=row[0],
                produto_id=row[1],
                quantidade=row[2],
                medida=row[3],
                descricao=row[4],
                valor_unitario=row[5],
                valor_total=row[6],
                categoria=row[7],
                classificacao=row[8],
                user_id=row[9]
            ))
        if self.conn is None:
            conn.close()
        return itens

    def get_itens_by_categoria(self, categoria: str, user_id: int) -> list[ItemCusto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM itens_custo 
            WHERE categoria = ? AND user_id = ?
            ORDER BY produto_id, descricao
        """, (categoria, user_id))
        rows = cursor.fetchall()
        itens = []
        for row in rows:
            itens.append(ItemCusto(
                item_id=row[0],
                produto_id=row[1],
                quantidade=row[2],
                medida=row[3],
                descricao=row[4],
                valor_unitario=row[5],
                valor_total=row[6],
                categoria=row[7],
                classificacao=row[8],
                user_id=row[9]
            ))
        if self.conn is None:
            conn.close()
        return itens

    def get_itens_by_classificacao(self, classificacao: str, user_id: int) -> list[ItemCusto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM itens_custo 
            WHERE classificacao = ? AND user_id = ?
            ORDER BY produto_id, categoria, descricao
        """, (classificacao, user_id))
        rows = cursor.fetchall()
        itens = []
        for row in rows:
            itens.append(ItemCusto(
                item_id=row[0],
                produto_id=row[1],
                quantidade=row[2],
                medida=row[3],
                descricao=row[4],
                valor_unitario=row[5],
                valor_total=row[6],
                categoria=row[7],
                classificacao=row[8],
                user_id=row[9]
            ))
        if self.conn is None:
            conn.close()
        return itens

    def get_total_by_produto(self, produto_id: str, user_id: int) -> float:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(valor_total) FROM itens_custo 
            WHERE produto_id = ? AND user_id = ?
        """, (produto_id, user_id))
        total = cursor.fetchone()[0] or 0.0
        if self.conn is None:
            conn.close()
        return total

    def get_total_by_categoria(self, categoria: str, user_id: int) -> float:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(valor_total) FROM itens_custo 
            WHERE categoria = ? AND user_id = ?
        """, (categoria, user_id))
        total = cursor.fetchone()[0] or 0.0
        if self.conn is None:
            conn.close()
        return total