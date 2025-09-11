from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QMessageBox, QTableView,
                               QComboBox, QSpinBox, QHeaderView, QGroupBox,
                               QRadioButton, QScrollArea, QFormLayout)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QFont
from PySide6.QtCore import Qt
from model.Session import Session
from model.ItemCustoRepository import ItemCustoRepository

class CusteioProdutoWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.item_custo_repo = ItemCustoRepository()
        self.volume_inputs = {}  # Dicionário para guardar os widgets de volume
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
        title = QLabel("Relatório de Custeio de Produtos")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # --- PASSO 1: Volumes de Produção ---
        group_volumes = QGroupBox("Passo 1: Definir Volumes de Produção")
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout_volumes = QFormLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        group_volumes_layout = QVBoxLayout()
        group_volumes_layout.addWidget(scroll_area)
        group_volumes.setLayout(group_volumes_layout)
        main_layout.addWidget(group_volumes)
        # --- PASSO 3: Critério de Rateio CIF (oculto por padrão) ---
        self.group_cif_rateio = QGroupBox("Passo 3: Escolher Critério de Rateio dos Custos Indiretos")
        cif_rateio_layout = QHBoxLayout()
        self.combo_cif_criterio = QComboBox()
        self.combo_cif_criterio.addItems(["Mão de Obra Direta (MOD)", "Material Direto (MD)", "Volume Produzido", "MOD + MD"])
        cif_rateio_layout.addWidget(QLabel("Ratear CIF com base em:"))
        cif_rateio_layout.addWidget(self.combo_cif_criterio)
        self.group_cif_rateio.setLayout(cif_rateio_layout)
        main_layout.addWidget(self.group_cif_rateio)
        self.group_cif_rateio.setVisible(False)

        # --- PASSO 2: Princípio de Custeio ---
        group_principio = QGroupBox("Passo 2: Escolher Princípio de Custeio")
        principio_layout = QHBoxLayout()
        self.radio_variavel = QRadioButton("Variável")
        self.radio_integral = QRadioButton("Integral ")
        self.radio_ideal = QRadioButton("Ideal")
        self.radio_variavel.toggled.connect(lambda: self.toggle_cif_rateio_group(False))
        self.radio_integral.toggled.connect(lambda: self.toggle_cif_rateio_group(True))
        self.radio_ideal.toggled.connect(lambda: self.toggle_cif_rateio_group(True))
        principio_layout.addWidget(self.radio_variavel)
        principio_layout.addWidget(self.radio_integral)
        principio_layout.addWidget(self.radio_ideal)
        group_principio.setLayout(principio_layout)
        main_layout.addWidget(group_principio)
        self.radio_variavel.setChecked(True)


        # --- Botão de Ação ---
        btn_gerar = QPushButton("Gerar Relatório")
        btn_gerar.setStyleSheet("background-color: #28a745; color: white; font-size: 14px; padding: 5px;")
        btn_gerar.clicked.connect(self.gerar_relatorio)
        main_layout.addWidget(btn_gerar)
        
        # --- Tabela de Resultados ---
        self.table_report = QTableView()
        self.model = QStandardItemModel()
        self.table_report.setModel(self.model)
        self.table_report.setEditTriggers(QTableView.NoEditTriggers)
        self.table_report.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table_report)

    def load_data(self):
        """Carrega os dados iniciais, como a lista de produtos."""
        self.populate_volumes_form()
        self.model.clear()

    def populate_volumes_form(self):
        """Cria dinamicamente os campos de input para o volume de cada produto."""
        # Limpa widgets antigos
        while self.form_layout_volumes.count():
            item = self.form_layout_volumes.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.volume_inputs.clear()
        user_id = Session().user_id
        if not user_id: return

        try:
            produtos = self.item_custo_repo.get_distinct_produto_ids(user_id)
            # Regra crucial: ignorar o produto "nenhum"
            produtos_filtrados = [p for p in produtos if p.lower() != 'nenhum']

            for produto_id in produtos_filtrados:
                spin_box = QSpinBox()
                spin_box.setRange(0, 999999)
                spin_box.setValue(100) # Valor padrão
                self.form_layout_volumes.addRow(QLabel(f"Volume para {produto_id}:"), spin_box)
                self.volume_inputs[produto_id] = spin_box
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar a lista de produtos: {e}")

    def toggle_cif_rateio_group(self, visible):
        """Mostra ou oculta a seção de critérios de rateio do CIF."""
        self.group_cif_rateio.setVisible(visible)

    def gerar_relatorio(self):
        """Ponto de entrada principal que orquestra a coleta de dados e os cálculos."""
        user_id = Session().user_id
        if not user_id: return

        # Coleta os volumes informados pelo usuário
        volumes = {pid: spinbox.value() for pid, spinbox in self.volume_inputs.items()}
        if not any(v > 0 for v in volumes.values()):
            QMessageBox.warning(self, "Atenção", "Informe um volume de produção maior que zero para ao menos um produto.")
            return

        try:
            # 1. Obter todos os itens de custo e separá-los
            all_items = self.item_custo_repo.get_itens_by_user(user_id)
            
            # Itens de overhead (CIF, CO) cadastrados no produto "nenhum"
            itens_overhead = [item for item in all_items if item.produto_id.lower() == 'nenhum']
            # Itens de custo direto, vinculados a produtos específicos
            itens_produtos = [item for item in all_items if item.produto_id.lower() != 'nenhum']

            # 2. Pré-calcular custos unitários diretos e variáveis para cada produto
            product_costs = {pid: {'MD': 0, 'MOD': 0, 'Variavel': 0} for pid in volumes.keys()}
            for item in itens_produtos:
                pid = item.produto_id
                if pid in product_costs:
                    if item.categoria == 'MD':
                        product_costs[pid]['MD'] += item.valor_total
                    elif item.categoria == 'MOD':
                        product_costs[pid]['MOD'] += item.valor_total
                    if item.classificacao == 'Variável':
                        product_costs[pid]['Variavel'] += item.valor_total

            # 3. Executar o cálculo com base no princípio selecionado
            if self.radio_variavel.isChecked():
                self.gerar_relatorio_variavel(product_costs, volumes)
            else: # Integral ou Ideal
                self.gerar_relatorio_absorcao(product_costs, volumes, itens_overhead)

        except Exception as e:
            QMessageBox.critical(self, "Erro no Cálculo", f"Ocorreu um erro ao gerar o relatório: {e}")

    def gerar_relatorio_variavel(self, product_costs, volumes):
        """
        Gera um relatório focado exclusivamente no Material Direto (MD),
        seguindo o formato da tabela solicitada.
        """
        self.model.clear()
        # Headers exatamente como na imagem de exemplo
        headers = [
            "Produto", 
            "Volume", 
            "MD (R$)", 
            "Custo unitário (R$/Unid)"
        ]
        self.model.setHorizontalHeaderLabels(headers)

        bold_font = QFont()
        bold_font.setBold(True)

        total_geral_volume = 0
        total_geral_custo_md = 0

        for pid, vol in volumes.items():
            if vol == 0: continue

            # Calcula o custo total de MD para o volume informado
            custo_total_md_para_volume = product_costs[pid]['MD']

            # Pega apenas o custo unitário de Material Direto (MD) do produto
            custo_unit_md = custo_total_md_para_volume / vol
            
            # Acumula os totais para a linha de resumo
            total_geral_volume += vol
            total_geral_custo_md += custo_total_md_para_volume

            # Formata os números para o padrão brasileiro (ponto como separador de milhar, vírgula para decimal)
            volume_str = f"{vol:,.0f}".replace(",", ".")
            custo_total_str = f"{custo_total_md_para_volume:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            custo_unit_str = f"{custo_unit_md:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            row = [
                QStandardItem(pid),
                QStandardItem(volume_str),
                QStandardItem(custo_total_str),
                QStandardItem(custo_unit_str)
            ]
            
            # Alinha os números à direita para melhor visualização
            row[1].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row[2].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row[3].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.model.appendRow(row)
        
        # Adiciona a linha de TOTAL ao final
        volume_total_str = f"{total_geral_volume:,.0f}".replace(",", ".")
        custo_md_total_str = f"{total_geral_custo_md:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        total_row = [
            QStandardItem("TOTAL"),
            QStandardItem(volume_total_str),
            QStandardItem(custo_md_total_str),
            QStandardItem("-")
        ]
        
        for item in total_row:
            item.setFont(bold_font)
        
        total_row[1].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        total_row[2].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        total_row[3].setTextAlignment(Qt.AlignCenter)

        self.model.appendRow(total_row)

        self.table_report.resizeColumnsToContents()

    def gerar_relatorio_absorcao(self, product_costs, volumes, itens_overhead):
        """Gera a tabela para Custeio por Absorção (Integral e Ideal)."""
        criterio = self.combo_cif_criterio.currentText()
        is_ideal = self.radio_ideal.isChecked()

        # Calcula os "potes" de custos indiretos da empresa
        total_cif_pool = sum(item.valor_total for item in itens_overhead if item.categoria == 'CIF')
        total_co_pool = sum(item.valor_total for item in itens_overhead if item.categoria == 'CO')

        # Calcula a base total para o rateio
        base_total_rateio = 0
        if criterio == "Mão de Obra Direta (MOD)":
            base_total_rateio = sum(product_costs[pid]['MOD'] * vol for pid, vol in volumes.items())
        elif criterio == "Material Direto (MD)":
            base_total_rateio = sum(product_costs[pid]['MD'] * vol for pid, vol in volumes.items())
        elif criterio == "Volume Produzido":
            base_total_rateio = sum(volumes.values())
        elif criterio == "MOD + MD":
            base_total_rateio = sum((product_costs[pid]['MOD'] + product_costs[pid]['MD']) * vol for pid, vol in volumes.items())

        if base_total_rateio == 0:
            QMessageBox.warning(self, "Atenção", "A base de rateio calculada é zero. Não é possível ratear os custos indiretos.")
            return

        # Calcula as taxas de rateio
        taxa_cif = total_cif_pool / base_total_rateio
        taxa_co = total_co_pool / base_total_rateio

        # Prepara a tabela
        self.model.clear()
        headers = ["Produto", "Vol", "MD", "MOD", "CIF Rateado", "Custo Unitário"]
        if is_ideal:
            headers.insert(5, "CO Rateado")
        self.model.setHorizontalHeaderLabels(headers)

        for pid, vol in volumes.items():
            if vol == 0: continue
            
            custos = product_costs[pid]
            base_produto = 0
            if criterio == "Mão de Obra Direta (MOD)":
                base_produto = custos['MOD']
            elif criterio == "Material Direto (MD)":
                base_produto = custos['MD']
            elif criterio == "Volume Produzido":
                base_produto = 1 # O rateio é por unidade
            elif criterio == "MOD + MD":
                base_produto = custos['MOD'] + custos['MD']

            # Calcula os custos rateados por unidade
            cif_unit_rateado = base_produto * taxa_cif
            co_unit_rateado = base_produto * taxa_co if is_ideal else 0
            
            custo_unit_total = (custos['MD'] + custos['MOD'] + cif_unit_rateado + co_unit_rateado)/vol

            row = [
                QStandardItem(pid),
                QStandardItem(str(vol)),
                QStandardItem(f"R$ {custos['MD']:.2f}"),
                QStandardItem(f"R$ {custos['MOD']:.2f}"),
                QStandardItem(f"R$ {cif_unit_rateado:.2f}")
            ]
            if is_ideal:
                row.append(QStandardItem(f"R$ {co_unit_rateado:.2f}"))
            
            row.append(QStandardItem(f"R$ {custo_unit_total:.2f}"))
            self.model.appendRow(row)
    def logout_and_switch_to_welcome(self):
        self.stacked_widget.setCurrentIndex(0)