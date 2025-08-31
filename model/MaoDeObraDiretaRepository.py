import sqlite3
from model.MaoDeObraDireta import MaoDeObraDireta

class MaoDeObraDiretaRepository:
    def __init__(self, db_path="model/LoginSystem.db", conn=None):
        self.db_path = db_path
        self.conn = conn

    def get_connection(self):
        if self.conn:
            return self.conn
        return sqlite3.connect(self.db_path)

    def create_dbMOD(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mao_de_obra_direta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cargo TEXT NOT NULL,
                centro_custo TEXT NOT NULL,
                operacao TEXT NOT NULL,
                tempo_padrao REAL NOT NULL,
                capacidade_horas REAL NOT NULL,
                capacidade_itens INTEGER NOT NULL,
                custo_hora REAL NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
        if self.conn is None:
            conn.close()

    def add_mod(self, mod: MaoDeObraDireta) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mao_de_obra_direta 
            (cargo, centro_custo, operacao, tempo_padrao, capacidade_horas, capacidade_itens, custo_hora, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mod.cargo,
            mod.centro_custo,
            mod.operacao,
            mod.tempo_padrao,
            mod.capacidade_horas,
            mod.capacidade_itens,
            mod.custo_hora,
            mod.user_id
        ))
        mod_id = cursor.lastrowid
        conn.commit()
        if self.conn is None:
            conn.close()
        return mod_id

    def get_mod(self, mod_id: int, user_id: int) -> MaoDeObraDireta:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM mao_de_obra_direta 
            WHERE id = ? AND user_id = ?
        """, (mod_id, user_id))
        row = cursor.fetchone()
        
        if row:
            mod = MaoDeObraDireta(
                mod_id=row[0],
                cargo=row[1],
                centro_custo=row[2],
                operacao=row[3],
                tempo_padrao=row[4],
                capacidade_horas=row[5],
                capacidade_itens=row[6],
                custo_hora=row[7],
                user_id=row[8]
            )
            if self.conn is None:
                conn.close()
            return mod
        if self.conn is None:
            conn.close()
        return None

    def get_all_mod_by_user(self, user_id: int) -> list[MaoDeObraDireta]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM mao_de_obra_direta 
            WHERE user_id = ? 
            ORDER BY cargo, centro_custo
        """, (user_id,))
        rows = cursor.fetchall()
        mods = []
        for row in rows:
            mods.append(MaoDeObraDireta(
                mod_id=row[0],
                cargo=row[1],
                centro_custo=row[2],
                operacao=row[3],
                tempo_padrao=row[4],
                capacidade_horas=row[5],
                capacidade_itens=row[6],
                custo_hora=row[7],
                user_id=row[8]
            ))
        if self.conn is None:
            conn.close()
        return mods

    def update_mod(self, mod: MaoDeObraDireta) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE mao_de_obra_direta 
            SET cargo = ?,
                centro_custo = ?,
                operacao = ?,
                tempo_padrao = ?,
                capacidade_horas = ?,
                capacidade_itens = ?,
                custo_hora = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        """, (
            mod.cargo,
            mod.centro_custo,
            mod.operacao,
            mod.tempo_padrao,
            mod.capacidade_horas,
            mod.capacidade_itens,
            mod.custo_hora,
            mod.id,
            mod.user_id
        ))
        updated = cursor.rowcount > 0
        conn.commit()
        if self.conn is None:
            conn.close()
        return updated

    def delete_mod(self, mod_id: int, user_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM mao_de_obra_direta 
            WHERE id = ? AND user_id = ?
        """, (mod_id, user_id))
        deleted = cursor.rowcount > 0
        conn.commit()
        if self.conn is None:
            conn.close()
        return deleted

    def search_mod(self, search_term: str, user_id: int) -> list[MaoDeObraDireta]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM mao_de_obra_direta 
            WHERE (cargo LIKE ? OR centro_custo LIKE ? OR operacao LIKE ?) 
            AND user_id = ?
            ORDER BY cargo, centro_custo
        """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', user_id))
        rows = cursor.fetchall()
        mods = []
        for row in rows:
            mods.append(MaoDeObraDireta(
                mod_id=row[0],
                cargo=row[1],
                centro_custo=row[2],
                operacao=row[3],
                tempo_padrao=row[4],
                capacidade_horas=row[5],
                capacidade_itens=row[6],
                custo_hora=row[7],
                user_id=row[8]
            ))
        if self.conn is None:
            conn.close()
        return mods

    def get_mod_by_centro_custo(self, centro_custo: str, user_id: int) -> list[MaoDeObraDireta]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM mao_de_obra_direta 
            WHERE centro_custo = ? AND user_id = ?
            ORDER BY cargo
        """, (centro_custo, user_id))
        rows = cursor.fetchall()
        mods = []
        for row in rows:
            mods.append(MaoDeObraDireta(
                mod_id=row[0],
                cargo=row[1],
                centro_custo=row[2],
                operacao=row[3],
                tempo_padrao=row[4],
                capacidade_horas=row[5],
                capacidade_itens=row[6],
                custo_hora=row[7],
                user_id=row[8]
            ))
        if self.conn is None:
            conn.close()
        return mods

    def get_mod_by_cargo(self, cargo: str, user_id: int) -> list[MaoDeObraDireta]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM mao_de_obra_direta 
            WHERE cargo = ? AND user_id = ?
            ORDER BY centro_custo
        """, (cargo, user_id))
        rows = cursor.fetchall()
        mods = []
        for row in rows:
            mods.append(MaoDeObraDireta(
                mod_id=row[0],
                cargo=row[1],
                centro_custo=row[2],
                operacao=row[3],
                tempo_padrao=row[4],
                capacidade_horas=row[5],
                capacidade_itens=row[6],
                custo_hora=row[7],
                user_id=row[8]
            ))
        if self.conn is None:
            conn.close()
        return mods