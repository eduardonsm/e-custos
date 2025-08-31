import sqlite3
from model.CentroCusto import CentroCusto

class CentroCustoRepository:
    def __init__(self, db_path="model/LoginSystem.db", conn=None):
        self.db_path = db_path
        self.conn = conn

    def get_connection(self):
        if self.conn:
            return self.conn
        return sqlite3.connect(self.db_path)

    def create_dbCentrosCusto(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS centros_custo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('Produtivo', 'Auxiliar', 'Administrativo')),
                quantidade_postos INTEGER NOT NULL,
                capacidade_horas REAL NOT NULL,
                capacidade_itens INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
        if self.conn is None:
            conn.close()

    def add_centro_custo(self, centro: CentroCusto) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO centros_custo 
            (descricao, tipo, quantidade_postos, capacidade_horas, capacidade_itens, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            centro.descricao,
            centro.tipo,
            centro.quantidade_postos,
            centro.capacidade_horas,
            centro.capacidade_itens,
            centro.user_id
        ))
        centro_id = cursor.lastrowid
        conn.commit()
        if self.conn is None:
            conn.close()
        return centro_id

    def get_centro_custo(self, centro_id: int, user_id: int) -> CentroCusto:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM centros_custo 
            WHERE id = ? AND user_id = ?
        """, (centro_id, user_id))
        row = cursor.fetchone()
        
        if row:
            centro = CentroCusto(
                centro_id=row[0],
                descricao=row[1],
                tipo=row[2],
                quantidade_postos=row[3],
                capacidade_horas=row[4],
                capacidade_itens=row[5],
                user_id=row[6]
            )
            if self.conn is None:
                conn.close()
            return centro
        if self.conn is None:
            conn.close()
        return None

    def get_centros_by_user(self, user_id: int) -> list[CentroCusto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM centros_custo 
            WHERE user_id = ? 
            ORDER BY descricao
        """, (user_id,))
        rows = cursor.fetchall()
        centros = []
        for row in rows:
            centros.append(CentroCusto(
                centro_id=row[0],
                descricao=row[1],
                tipo=row[2],
                quantidade_postos=row[3],
                capacidade_horas=row[4],
                capacidade_itens=row[5],
                user_id=row[6]
            ))
        if self.conn is None:
            conn.close()
        return centros

    def update_centro_custo(self, centro: CentroCusto) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE centros_custo 
            SET descricao = ?,
                tipo = ?,
                quantidade_postos = ?,
                capacidade_horas = ?,
                capacidade_itens = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        """, (
            centro.descricao,
            centro.tipo,
            centro.quantidade_postos,
            centro.capacidade_horas,
            centro.capacidade_itens,
            centro.id,
            centro.user_id
        ))
        updated = cursor.rowcount > 0
        conn.commit()
        if self.conn is None:
            conn.close()
        return updated

    def delete_centro_custo(self, centro_id: int, user_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM centros_custo 
            WHERE id = ? AND user_id = ?
        """, (centro_id, user_id))
        deleted = cursor.rowcount > 0
        conn.commit()
        if self.conn is None:
            conn.close()
        return deleted

    def search_centros(self, search_term: str, user_id: int) -> list[CentroCusto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM centros_custo 
            WHERE descricao LIKE ? AND user_id = ?
            ORDER BY descricao
        """, (f'%{search_term}%', user_id))
        rows = cursor.fetchall()
        centros = []
        for row in rows:
            centros.append(CentroCusto(
                centro_id=row[0],
                descricao=row[1],
                tipo=row[2],
                quantidade_postos=row[3],
                capacidade_horas=row[4],
                capacidade_itens=row[5],
                user_id=row[6]
            ))
        if self.conn is None:
            conn.close()
        return centros

    def get_centros_by_tipo(self, tipo: str, user_id: int) -> list[CentroCusto]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM centros_custo 
            WHERE tipo = ? AND user_id = ?
            ORDER BY descricao
        """, (tipo, user_id))
        rows = cursor.fetchall()
        centros = []
        for row in rows:
            centros.append(CentroCusto(
                centro_id=row[0],
                descricao=row[1],
                tipo=row[2],
                quantidade_postos=row[3],
                capacidade_horas=row[4],
                capacidade_itens=row[5],
                user_id=row[6]
            ))
        if self.conn is None:
            conn.close()
        return centros