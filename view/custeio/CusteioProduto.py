from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QMessageBox, QTableView,
                               QComboBox, QSpinBox, QHeaderView)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QFont
from PySide6.QtCore import Qt
from model.Session import Session
from model.ItemCustoRepository import ItemCustoRepository

class CusteioProdutoWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.item_custo_repo = ItemCustoRepository()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Cabeçalho (Padrão) ---
        header_layout = QHBoxLayout()
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        header_layout.addStretch(1)
        home_button = QPushButton("Início")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        header_layout.addWidget(home_button)
        sair_button = QPushButton("Sair")
        sair_button.clicked.connect(self.logout_and_switch_to_welcome)
        header_layout.addWidget(sair_button)
        self.perfil_label = QLabel()
        header_layout.addWidget(self.perfil_label)
        main_layout.addLayout(header_layout)

        # --- Divisória (Padrão) ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # --- Título ---
        title = QLabel("Cálculo de Custo do Produto (Custeio por Absorção)")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # --- Controles de Entrada do Usuário ---
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(10, 10, 10, 20)
        
        input_layout.addWidget(QLabel("Produto ID:"))
        self.combo_produto_id = QComboBox()
        input_layout.addWidget(self.combo_produto_id)
        
        input_layout.addSpacing(20)
        
        input_layout.addWidget(QLabel("Volume de Produção:"))
        self.spin_volume = QSpinBox()
        self.spin_volume.setRange(1, 999999)
        self.spin_volume.setValue(100) # Valor inicial
        input_layout.addWidget(self.spin_volume)
        
        input_layout.addStretch()
        
        btn_calcular = QPushButton("Calcular Custo")
        btn_calcular.setStyleSheet("background-color: #007BFF; color: white;")
        btn_calcular.clicked.connect(self.calcular_custo)
        input_layout.addWidget(btn_calcular)
        
        main_layout.addLayout(input_layout)

        # --- Tabela de Resultados ---
        self.table_custeio = QTableView()
        self.model = QStandardItemModel()
        self.table_custeio.setModel(self.model)
        self.table_custeio.setEditTriggers(QTableView.NoEditTriggers)
        self.table_custeio.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table_custeio)

        # --- Resumo dos Custos ---
        summary_layout = QHBoxLayout()
        summary_layout.addStretch()
        
        self.lbl_custo_unitario = QLabel("Custo Unitário Total: R$ 0.00")
        self.lbl_custo_unitario.setStyleSheet("font-size: 14px; font-weight: bold;")
        summary_layout.addWidget(self.lbl_custo_unitario)
        
        summary_layout.addSpacing(40)
        
        self.lbl_custo_total_volume = QLabel("Custo Total para o Volume: R$ 0.00")
        self.lbl_custo_total_volume.setStyleSheet("font-size: 14px; font-weight: bold; color: #28a745;")
        summary_layout.addWidget(self.lbl_custo_total_volume)
        
        main_layout.addLayout(summary_layout)
    
    def load_data(self):
        """Carrega os dados necessários para a view, como a lista de produtos."""
        self.update_user_info()
        self.popular_produtos_combobox()
        self.model.clear() # Limpa resultados anteriores
        self.lbl_custo_unitario.setText("Custo Unitário Total: R$ 0.00")
        self.lbl_custo_total_volume.setText("Custo Total para o Volume: R$ 0.00")

    def popular_produtos_combobox(self):
        """Busca e preenche a lista de produtos que podem ser custeados."""
        self.combo_produto_id.clear()
        user_id = Session().user_id
        if not user_id:
            return
        try:
            produtos = self.item_custo_repo.get_distinct_produto_ids(user_id)
            if produtos:
                self.combo_produto_id.addItems(produtos)
            else:
                self.combo_produto_id.addItem("Nenhum produto com custos")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar a lista de produtos: {e}")

    def calcular_custo(self):
        """Executa toda a lógica de cálculo do custeio por absorção."""
        user_id = Session().user_id
        produto_id = self.combo_produto_id.currentText()
        volume = self.spin_volume.value()

        if not user_id or not produto_id or produto_id == "Nenhum produto com custos":
            QMessageBox.warning(self, "Atenção", "Selecione um produto válido para calcular.")
            return

        try:
            # 1. Obter todos os itens para calcular totais da empresa (base do rateio)
            todos_itens = self.item_custo_repo.get_itens_by_user(user_id)
            total_mod_empresa = sum(item.valor_total for item in todos_itens if item.categoria == 'MOD')
            total_cif_empresa = sum(item.valor_total for item in todos_itens if item.categoria == 'CIF')
            
            # 2. Calcular a taxa de rateio do CIF
            taxa_cif = (total_cif_empresa / total_mod_empresa) if total_mod_empresa > 0 else 0
            
            # 3. Obter os itens do produto específico para calcular seus custos diretos
            itens_produto = self.item_custo_repo.get_itens_by_produto(produto_id, user_id)
            custo_unitario_md = sum(item.valor_total for item in itens_produto if item.categoria == 'MD')
            custo_unitario_mod = sum(item.valor_total for item in itens_produto if item.categoria == 'MOD')
            custo_unitario_co = sum(item.valor_total for item in itens_produto if item.categoria == 'CO')
            
            # 4. Ratear o CIF para o produto
            custo_unitario_cif = custo_unitario_mod * taxa_cif
            
            # 5. Calcular totais
            custo_unitario_total = custo_unitario_md + custo_unitario_mod + custo_unitario_cif + custo_unitario_co
            custo_total_volume = custo_unitario_total * volume

            # 6. Exibir resultados na tabela
            self.popular_tabela_resultados({
                "MD": custo_unitario_md,
                "MOD": custo_unitario_mod,
                "CIF": custo_unitario_cif,
                "CO": custo_unitario_co
            }, volume)
            
            # 7. Atualizar os labels de resumo
            self.lbl_custo_unitario.setText(f"Custo Unitário Total: R$ {custo_unitario_total:.2f}")
            self.lbl_custo_total_volume.setText(f"Custo Total para {volume} unids: R$ {custo_total_volume:.2f}")

        except Exception as e:
            QMessageBox.critical(self, "Erro de Cálculo", f"Ocorreu um erro ao calcular os custos:\n{e}")
            
    def popular_tabela_resultados(self, custos_unitarios: dict, volume: int):
        self.model.clear()
        headers = ["Componente de Custo", "Valor Unitário (R$)", f"Valor Total p/ {volume} unids (R$)"]
        self.model.setHorizontalHeaderLabels(headers)
        
        bold_font = QFont()
        bold_font.setBold(True)
        
        total_unitario = 0
        total_volume = 0
        
        for nome, valor_unit in custos_unitarios.items():
            valor_volume = valor_unit * volume
            total_unitario += valor_unit
            total_volume += valor_volume
            
            row = [
                QStandardItem(nome),
                QStandardItem(f"{valor_unit:.4f}"),
                QStandardItem(f"{valor_volume:.2f}")
            ]
            self.model.appendRow(row)
        
        # Linha de Total
        total_row = [
            QStandardItem("CUSTO TOTAL"),
            QStandardItem(f"{total_unitario:.4f}"),
            QStandardItem(f"{total_volume:.2f}")
        ]
        
        for item in total_row:
            item.setFont(bold_font)
            
        self.model.appendRow(total_row)


    def logout_and_switch_to_welcome(self):
        Session().clear_session()
        self.stacked_widget.setCurrentIndex(0)

    def update_user_info(self):
        session = Session()
        username = session.username if session.username else "Não conectado"
        self.perfil_label.setText(f"Usuário: {username}")