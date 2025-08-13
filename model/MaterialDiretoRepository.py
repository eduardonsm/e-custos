import sqlite3
from model.MaterialDireto import MaterialDireto

class MaterialDiretoRepository:
    def __init__(self, db_path="model/LoginSystem.db", conn=None):
        self.db_path = db_path
        self.conn = conn

    def get_connection(self):
        if self.conn:
            return self.conn
        return sqlite3.connect(self.db_path)

    def create_dbMaterials(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materiais_diretos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                fonte TEXT NOT NULL CHECK(fonte IN ('Fornecido', 'Produzido')),
                lead_time_producao TEXT NOT NULL,
                lead_time_fornecimento TEXT NOT NULL,
                fornecedor TEXT NOT NULL,
                valor_unitario REAL NOT NULL,
                estoque_atual INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                estoque_maximo INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
        if self.conn is None:
            conn.close()

    def add_material(self, material: MaterialDireto) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO materiais_diretos 
            (descricao, fonte, lead_time_producao, lead_time_fornecimento, 
             fornecedor, valor_unitario, estoque_atual, estoque_minimo, 
             estoque_maximo, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            material.descricao,
            material.fonte,
            material.lead_time_producao,
            material.lead_time_fornecimento,
            material.fornecedor,
            material.valor_unitario,
            material.estoque_atual,
            material.estoque_minimo,
            material.estoque_maximo,
            material.user_id
        ))
        material_id = cursor.lastrowid
        conn.commit()
        if self.conn is None:
            conn.close()
        return material_id

    def get_material(self, material_id: int, user_id: int) -> MaterialDireto:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM materiais_diretos 
            WHERE id = ? AND user_id = ?
        """, (material_id, user_id))
        row = cursor.fetchone()
        
        if row:
            material = MaterialDireto(
                material_id=row[0],
                descricao=row[1],
                fonte=row[2],
                lead_time_producao=row[3],
                lead_time_fornecimento=row[4],
                fornecedor=row[5],
                valor_unitario=row[6],
                estoque_atual=row[7],
                estoque_minimo=row[8],
                estoque_maximo=row[9],
                user_id=row[10]
            )
            if self.conn is None:
                conn.close()
            return material
        if self.conn is None:
            conn.close()
        return None

    def get_materiais_by_user(self, user_id: int) -> list[MaterialDireto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM materiais_diretos 
            WHERE user_id = ? 
            ORDER BY descricao
        """, (user_id,))
        rows = cursor.fetchall()
        materiais = []
        for row in rows:
            materiais.append(MaterialDireto(
                material_id=row[0],
                descricao=row[1],
                fonte=row[2],
                lead_time_producao=row[3],
                lead_time_fornecimento=row[4],
                fornecedor=row[5],
                valor_unitario=row[6],
                estoque_atual=row[7],
                estoque_minimo=row[8],
                estoque_maximo=row[9],
                user_id=row[10]
            ))
        if self.conn is None:
            conn.close()
        return materiais

    def update_material(self, material: MaterialDireto) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE materiais_diretos 
            SET descricao = ?,
                fonte = ?,
                lead_time_producao = ?,
                lead_time_fornecimento = ?,
                fornecedor = ?,
                valor_unitario = ?,
                estoque_atual = ?,
                estoque_minimo = ?,
                estoque_maximo = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        """, (
            material.descricao,
            material.fonte,
            material.lead_time_producao,
            material.lead_time_fornecimento,
            material.fornecedor,
            material.valor_unitario,
            material.estoque_atual,
            material.estoque_minimo,
            material.estoque_maximo,
            material.id,
            material.user_id
        ))
        updated = cursor.rowcount > 0
        conn.commit()
        if self.conn is None:
            conn.close()
        return updated

    def delete_material(self, material_id: int, user_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM materiais_diretos 
            WHERE id = ? AND user_id = ?
        """, (material_id, user_id))
        deleted = cursor.rowcount > 0
        conn.commit()
        if self.conn is None:
            conn.close()
        return deleted

    def search_materiais(self, search_term: str, user_id: int) -> list[MaterialDireto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM materiais_diretos 
            WHERE (descricao LIKE ? OR fornecedor LIKE ?) 
            AND user_id = ?
            ORDER BY descricao
        """, (f'%{search_term}%', f'%{search_term}%', user_id))
        rows = cursor.fetchall()
        materiais = []
        for row in rows:
            materiais.append(MaterialDireto(
                material_id=row[0],
                descricao=row[1],
                fonte=row[2],
                lead_time_producao=row[3],
                lead_time_fornecimento=row[4],
                fornecedor=row[5],
                valor_unitario=row[6],
                estoque_atual=row[7],
                estoque_minimo=row[8],
                estoque_maximo=row[9],
                user_id=row[10]
            ))
        if self.conn is None:
            conn.close()
        return materiais