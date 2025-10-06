import sqlite3
import os

def popular_banco_dados():
    """
    Conecta ao banco de dados e executa o script SQL para inserir os dados iniciais.
    """
    # Garante que o caminho para o banco de dados esteja correto
    db_path = os.path.join("model", "LoginSystem.db")
    
    # O script SQL completo que você quer executar
    sql_script = """
    -- Apaga os dados antigos do usuário 1 para evitar duplicatas
    DELETE FROM itens_custo WHERE user_id = 1;

    -- Inicia a inserção dos novos dados
    BEGIN TRANSACTION;

    -- Inserção para o produto CV-001
    INSERT INTO itens_custo (produto_id, quantidade, medida, descricao, valor_unitario, valor_total, categoria, classificacao, user_id) VALUES
    ('CV-001', 10000, 'Unid', 'Tampa da ponta', 0.25, 2500.00, 'MD', 'Variável', 1),
    ('CV-001', 10000, 'Unid', 'Tampa superior', 0.10, 1000.00, 'MD', 'Variável', 1),
    ('CV-001', 10000, 'Unid', 'Corpo', 0.40, 4000.00, 'MD', 'Variável', 1),
    ('CV-001', 10000, 'Unid', 'Tubo interno', 0.15, 1500.00, 'MD', 'Variável', 1),
    ('CV-001', 50000, 'ml', 'Tinta vermelha', 0.05, 2500.00, 'MD', 'Variável', 1),
    ('CV-001', 100, 'Unid', 'Embalagem', 0.15, 15.00, 'MD', 'Variável', 1),
    ('CV-001', 1, 'Unid', 'Salário do almox', 650.00, 650.00, 'MOD', 'Fixo', 1),
    ('CV-001', 1, 'Unid', 'Salário do injetor', 650.00, 650.00, 'MOD', 'Fixo', 1),
    ('CV-001', 1, 'Unid', 'Salário do montador', 650.00, 650.00, 'MOD', 'Fixo', 1),
    ('CV-001', 1, 'Unid', 'Salário do embalador', 650.00, 650.00, 'MOD', 'Fixo', 1);

    -- Inserção para o produto CA-002
    INSERT INTO itens_custo (produto_id, quantidade, medida, descricao, valor_unitario, valor_total, categoria, classificacao, user_id) VALUES
    ('CA-002', 6000, 'Unid', 'Tampa da ponta', 0.25, 1500.00, 'MD', 'Variável', 1),
    ('CA-002', 6000, 'Unid', 'Tampa superior', 0.10, 600.00, 'MD', 'Variável', 1),
    ('CA-002', 6000, 'Unid', 'Corpo', 0.40, 2400.00, 'MD', 'Variável', 1),
    ('CA-002', 6000, 'Unid', 'Tubo interno', 0.15, 900.00, 'MD', 'Variável', 1),
    ('CA-002', 20000, 'ml', 'Tinta azul', 0.05, 1000.00, 'MD', 'Variável', 1),
    ('CA-002', 60, 'Unid', 'Embalagem', 0.15, 9.00, 'MD', 'Variável', 1),
    ('CA-002', 1, 'Unid', 'Salário do almox', 1100.00, 1100.00, 'MOD', 'Fixo', 1),
    ('CA-002', 1, 'Unid', 'Salário do injetor', 1100.00, 1100.00, 'MOD', 'Fixo', 1),
    ('CA-002', 1, 'Unid', 'Salário do montador', 1100.00, 1100.00, 'MOD', 'Fixo', 1),
    ('CA-002', 1, 'Unid', 'Salário do embalador', 1100.00, 1100.00, 'MOD', 'Fixo', 1);

    -- Inserção para o produto CP-003
    INSERT INTO itens_custo (produto_id, quantidade, medida, descricao, valor_unitario, valor_total, categoria, classificacao, user_id) VALUES
    ('CP-003', 12000, 'Unid', 'Tampa da ponta', 0.25, 3000.00, 'MD', 'Variável', 1),
    ('CP-003', 12000, 'Unid', 'Tampa superior', 0.10, 1200.00, 'MD', 'Variável', 1),
    ('CP-003', 12000, 'Unid', 'Corpo', 0.40, 4800.00, 'MD', 'Variável', 1),
    ('CP-003', 12000, 'Unid', 'Tubo interno', 0.15, 1800.00, 'MD', 'Variável', 1),
    ('CP-003', 60000, 'ml', 'Tinta Preta', 0.05, 3000.00, 'MD', 'Variável', 1),
    ('CP-003', 120, 'Unid', 'Embalagem', 0.15, 18.00, 'MD', 'Variável', 1),
    ('CP-003', 1, 'Unid', 'Salário do almox', 750.00, 750.00, 'MOD', 'Fixo', 1),
    ('CP-003', 1, 'Unid', 'Salário do injetor', 750.00, 750.00, 'MOD', 'Fixo', 1),
    ('CP-003', 1, 'Unid', 'Salário do montador', 750.00, 750.00, 'MOD', 'Fixo', 1),
    ('CP-003', 1, 'Unid', 'Salário do embalador', 750.00, 750.00, 'MOD', 'Fixo', 1);

    -- Inserção para o produto CD-004
    INSERT INTO itens_custo (produto_id, quantidade, medida, descricao, valor_unitario, valor_total, categoria, classificacao, user_id) VALUES
    ('CD-004', 8000, 'Unid', 'Tampa da ponta', 0.25, 2000.00, 'MD', 'Variável', 1),
    ('CD-004', 8000, 'Unid', 'Tampa superior', 0.10, 800.00, 'MD', 'Variável', 1),
    ('CD-004', 8000, 'Unid', 'Corpo', 0.40, 3200.00, 'MD', 'Variável', 1),
    ('CD-004', 8000, 'Unid', 'Tubo interno', 0.15, 1200.00, 'MD', 'Variável', 1),
    ('CD-004', 40000, 'ml', 'Tinta verde', 0.05, 2000.00, 'MD', 'Variável', 1),
    ('CD-004', 80, 'Unid', 'Embalagem', 0.15, 12.00, 'MD', 'Variável', 1),
    ('CD-004', 1, 'Unid', 'Salário do almox', 500.00, 500.00, 'MOD', 'Fixo', 1),
    ('CD-004', 1, 'Unid', 'Salário do injetor', 500.00, 500.00, 'MOD', 'Fixo', 1),
    ('CD-004', 1, 'Unid', 'Salário do montador', 500.00, 500.00, 'MOD', 'Fixo', 1),
    ('CD-004', 1, 'Unid', 'Salário do embalador', 500.00, 500.00, 'MOD', 'Fixo', 1);

    -- Inserção para os itens "Nenhum" (custos indiretos)
    INSERT INTO itens_custo (produto_id, quantidade, medida, descricao, valor_unitario, valor_total, categoria, classificacao, user_id) VALUES
    ('Nenhum', 1, 'Unid', 'Salário do supervisor', 3800.00, 3800.00, 'CIF', 'Fixo', 1),
    ('Nenhum', 1, 'Unid', 'Aluguel da área de produção', 4600.00, 4600.00, 'CIF', 'Fixo', 1),
    ('Nenhum', 1, 'Unid', 'Salário do limpador', 2600.00, 2600.00, 'CIF', 'Fixo', 1),
    ('Nenhum', 5, 'litros', 'Água sanitária', 5.00, 25.00, 'CIF', 'Fixo', 1),
    ('Nenhum', 10, 'kg', 'Sabão em pó', 8.00, 80.00, 'CIF', 'Fixo', 1),
    ('Nenhum', 25, 'litros', 'Desinfetante', 6.00, 150.00, 'CIF', 'Fixo', 1),
    ('Nenhum', 250, 'kW/h', 'Energia da produção', 15.00, 3750.00, 'CIF', 'Fixo', 1),
    ('Nenhum', 25, 'h', 'Paradas não planejadas', 15.00, 375.00, 'CO', 'Fixo', 1),
    ('Nenhum', 40, 'h', 'Capacidade ociosa', 20.00, 800.00, 'CO', 'Fixo', 1),
    ('Nenhum', 20, 'Unid', 'Retrabalho', 2.00, 40.00, 'CO', 'Fixo', 1);

    COMMIT;
    """

    conn = None # Inicializa a conexão como None
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Executando script para popular o banco de dados...")
        # Executa o script inteiro de uma vez
        cursor.executescript(sql_script)
        
        # Confirma as mudanças (embora o COMMIT já esteja no script, é uma boa prática)
        conn.commit()
        print("Dados inseridos com sucesso!")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao inserir os dados: {e}")
        if conn:
            conn.rollback() # Desfaz as mudanças em caso de erro

    finally:
        if conn:
            # Fecha a conexão
            conn.close()
            print("Conexão com o banco de dados fechada.")


# Executa a função principal
if __name__ == "__main__":
    popular_banco_dados()