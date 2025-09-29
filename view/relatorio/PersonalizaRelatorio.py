from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QLabel, QPushButton, QGroupBox, QCheckBox, QRadioButton, 
                               QButtonGroup, QDateEdit, QScrollArea, QComboBox, QTableView,
                               QFormLayout, QMessageBox, QSpinBox)
from PySide6.QtGui import QFont, QStandardItem, QStandardItemModel, QPainter
from PySide6.QtCore import Qt, QDate
from PySide6.QtCharts import QChartView, QChart, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis
from model.Session import Session
from model.ItemCustoRepository import ItemCustoRepository

class PersonalizaRelatorioWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.item_custo_repo = ItemCustoRepository()
        
        self.volume_inputs = {}
        self.product_checkboxes = {}
        self.category_checkboxes = {}

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #c5d4e8; font-size: 11px;")

        title = QLabel("Personalize seu relatório")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("background-color: white; border: 1px solid #555; border-radius: 5px; padding: 5px;")
        main_layout.addWidget(title, 0, Qt.AlignCenter)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        # A UI agora é dividida: 1º Seleção, 2º Volumes
        selection_and_volumes_layout = QVBoxLayout()
        selection_and_volumes_layout.addWidget(self._create_product_selection_group())
        selection_and_volumes_layout.addWidget(self._create_volumes_group())

        grid_layout.addLayout(selection_and_volumes_layout, 0, 0, 2, 1) # Ocupa 2 linhas de altura
        grid_layout.addWidget(self._create_period_group(), 0, 1)
        grid_layout.addWidget(self._create_category_group(), 0, 2)
        grid_layout.addWidget(self._create_principle_group(), 0, 3)
        
        grid_layout.addWidget(self._create_cif_rateio_group(), 1, 1)
        grid_layout.addWidget(self._create_classification_group(), 1, 2)
        grid_layout.addWidget(self._create_visualization_group(), 1, 3)
        
        main_layout.addLayout(grid_layout)

        btn_generate = QPushButton("Gerar relatório")
        btn_generate.setFont(QFont("Arial", 12, QFont.Bold))
        btn_generate.setStyleSheet("""
            QPushButton { background-color: #2c3e50; color: white; border-radius: 5px; padding: 10px; }
            QPushButton:hover { background-color: #34495e; }
        """)
        btn_generate.clicked.connect(self.generate_report)
        main_layout.addWidget(btn_generate, 0, Qt.AlignCenter)

        self.table_report = QTableView()
        self.model = QStandardItemModel()
        self.table_report.setModel(self.model)
        self.table_report.setEditTriggers(QTableView.NoEditTriggers)
        main_layout.addWidget(self.table_report)
        
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        main_layout.addWidget(self.chart_view)

    # --- Métodos de Criação dos Grupos da UI ---

    def _create_product_selection_group(self):
        group = QGroupBox("1. Selecione os Produtos")
        layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.product_selection_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        
        layout.addWidget(scroll_area)

        btn_confirmar_produtos = QPushButton("Confirmar Produtos e Definir Volumes")
        btn_confirmar_produtos.clicked.connect(self.update_volume_inputs)
        layout.addWidget(btn_confirmar_produtos)
        
        group.setLayout(layout)
        return group

    def _create_volumes_group(self):
        group = QGroupBox("2. Defina os Volumes")
        layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout_volumes = QFormLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        group.setLayout(layout)
        return group

    # ... (outros métodos de criação da UI permanecem os mesmos)
    def _create_period_group(self):
        group = QGroupBox("Período (Início e Fim)")
        layout = QVBoxLayout()
        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDate(QDate.currentDate().addYears(-5))
        self.date_fim = QDateEdit()
        self.date_fim.setCalendarPopup(True)
        self.date_fim.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Início:"))
        layout.addWidget(self.date_inicio)
        layout.addWidget(QLabel("Fim:"))
        layout.addWidget(self.date_fim)
        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_category_group(self):
        group = QGroupBox("Categoria")
        layout = QVBoxLayout()
        categories = ["MOD", "MD", "CIF", "CO"]
        
        self.chk_cat_todos = QCheckBox("Todos")
        self.chk_cat_todos.stateChanged.connect(self._toggle_all_categories)
        layout.addWidget(self.chk_cat_todos)
        
        for cat in categories:
            chk = QCheckBox(cat)
            self.category_checkboxes[cat] = chk
            layout.addWidget(chk)
            
        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_classification_group(self):
        group = QGroupBox("Classificação")
        layout = QVBoxLayout()
        self.chk_class_fixos = QCheckBox("C. Fixos")
        self.chk_class_variaveis = QCheckBox("C. Variáveis")
        layout.addWidget(self.chk_class_fixos)
        layout.addWidget(self.chk_class_variaveis)
        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_cif_rateio_group(self):
        group = QGroupBox("Base de rateio dos CIFs")
        layout = QVBoxLayout()
        self.combo_cif_criterio = QComboBox()
        self.combo_cif_criterio.addItems(["Mão de Obra Direta (MOD)", "Material Direto (MD)", "Volume Produzido", "MOD + MD"])
        layout.addWidget(self.combo_cif_criterio)
        group.setLayout(layout)
        group.setVisible(False)
        self.group_cif_rateio = group
        return group

    def _create_principle_group(self):
        group = QGroupBox("Princípio de custeio")
        layout = QVBoxLayout()
        self.principle_group = QButtonGroup(self)
        self.radio_variavel = QRadioButton("Variável")
        self.radio_integral = QRadioButton("Integral")
        self.radio_ideal = QRadioButton("Ideal")
        
        self.radio_variavel.toggled.connect(lambda checked: self.group_cif_rateio.setVisible(not checked))
        self.radio_integral.toggled.connect(lambda checked: self.group_cif_rateio.setVisible(checked))
        self.radio_ideal.toggled.connect(lambda checked: self.group_cif_rateio.setVisible(checked))

        self.principle_group.addButton(self.radio_variavel)
        self.principle_group.addButton(self.radio_integral)
        self.principle_group.addButton(self.radio_ideal)
        layout.addWidget(self.radio_variavel)
        layout.addWidget(self.radio_integral)
        layout.addWidget(self.radio_ideal)
        self.radio_variavel.setChecked(True)
        group.setLayout(layout)
        return group

    def _create_visualization_group(self):
        group = QGroupBox("Visualização de dados")
        layout = QVBoxLayout()
        self.chk_viz_tabelas = QCheckBox("Tabelas")
        self.chk_viz_graficos = QCheckBox("Gráficos")
        self.chk_viz_tabelas.setChecked(True)
        layout.addWidget(self.chk_viz_tabelas)
        layout.addWidget(self.chk_viz_graficos)
        layout.addStretch()
        group.setLayout(layout)
        return group
        
    # --- Lógica Principal ---
    
    def load_data(self):
        """Carrega dados dinâmicos ao exibir a janela."""
        self.populate_product_selection()

    def _toggle_all_products(self, state):
        for checkbox in self.product_checkboxes.values():
            if checkbox.text().lower() != "nenhum":
                checkbox.setChecked(bool(state))
    
    def _toggle_all_categories(self, state):
        for checkbox in self.category_checkboxes.values():
            checkbox.setChecked(bool(state))

    def populate_product_selection(self):
        """Popula a lista de checkboxes para seleção de produtos."""
        # Limpa checkboxes antigos
        for chk in self.product_checkboxes.values():
            self.product_selection_layout.removeWidget(chk)
            chk.deleteLater()
        self.product_checkboxes.clear()

        user_id = Session().user_id
        if not user_id: return
        try:
            produtos = self.item_custo_repo.get_distinct_produto_ids(user_id)
            
            # Adiciona o checkbox "Todos"
            self.chk_todos = QCheckBox("Todos")
            self.chk_todos.stateChanged.connect(self._toggle_all_products)
            self.product_selection_layout.addWidget(self.chk_todos)

            # Adiciona os produtos do banco
            for pid in produtos:
                chk = QCheckBox(pid)
                self.product_checkboxes[pid] = chk
                self.product_selection_layout.addWidget(chk)
                
            self.product_selection_layout.addStretch()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar a lista de produtos: {e}")

    def update_volume_inputs(self):
        """Cria os campos de volume baseados nos produtos selecionados."""
        # Limpa widgets de volume antigos
        while self.form_layout_volumes.count():
            self.form_layout_volumes.takeAt(0).widget().deleteLater()
        self.volume_inputs.clear()

        # Cria novos widgets de volume para cada produto checado
        for pid, chk in self.product_checkboxes.items():
            if chk.isChecked() and pid.lower() != 'nenhum': # Volumes não se aplicam ao 'nenhum'
                spin_box = QSpinBox()
                spin_box.setRange(0, 999999)
                spin_box.setValue(100)
                self.form_layout_volumes.addRow(QLabel(f"Volume para {pid}:"), spin_box)
                self.volume_inputs[pid] = spin_box

    def generate_report(self):
        """Orquestra a coleta de dados, cálculos e exibição dos relatórios."""
        user_id = Session().user_id
        if not user_id: return
        
        self.model.clear()
        if self.chart_view.chart():
            self.chart_view.setChart(QChart()) # Limpa o gráfico anterior

        # --- Coleta de Filtros ---
        volumes = {pid: spinbox.value() for pid, spinbox in self.volume_inputs.items()}
        selected_products = [pid for pid, chk in self.product_checkboxes.items() if chk.isChecked()]
        
        # Validação: verifica se algum produto foi selecionado e teve seu volume definido
        if not volumes:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione os produtos e clique em 'Confirmar Produtos' antes de gerar o relatório.")
            return
        if not any(v > 0 for v in volumes.values()):
            QMessageBox.warning(self, "Atenção", "Informe um volume maior que zero para ao menos um produto.")
            return

        try:
            all_items = self.item_custo_repo.get_itens_by_user(user_id)
            itens_overhead = [item for item in all_items if item.produto_id.lower() == 'nenhum']
            itens_produtos = [item for item in all_items if item.produto_id in volumes.keys()]

            product_costs = {pid: {'MD': 0, 'MOD': 0} for pid in volumes.keys()}
            for item in itens_produtos:
                pid = item.produto_id
                if pid in product_costs:
                    if item.categoria == 'MD':
                        product_costs[pid]['MD'] += item.valor_total
                    elif item.categoria == 'MOD':
                        product_costs[pid]['MOD'] += item.valor_total
            # --- Geração das Tabelas ---
            report_data = []
            if self.chk_viz_tabelas.isChecked():
                if self.radio_variavel.isChecked():
                    report_data = self.gerar_relatorio_variavel(product_costs, volumes)
                else:
                    report_data = self.gerar_relatorio_absorcao(product_costs, volumes, itens_overhead)

            # --- Geração dos Gráficos ---
            if self.chk_viz_graficos.isChecked():
                # Conta quantos produtos REAIS foram selecionados (ignora o "Nenhum")
                num_selected_products = len([p for p in selected_products if p.lower() != 'nenhum'])

                if num_selected_products == 0:
                    # Se nenhum produto foi marcado, mostra um gráfico de pizza GERAL da empresa
                    self._gerar_grafico_pizza_geral(all_items)
                elif num_selected_products == 1:
                    # Se apenas 1 produto foi marcado, mostra um gráfico de pizza da composição de custo dele
                    self._gerar_grafico_pizza_produto(report_data)
                else: # 2 ou mais produtos
                    # Se 2 ou mais produtos foram marcados, mostra um gráfico de barras comparativo
                    self._gerar_grafico_barras(report_data)

        except Exception as e:
            QMessageBox.critical(self, "Erro no Cálculo", f"Ocorreu um erro ao gerar o relatório: {e}")

    def gerar_relatorio_variavel(self, product_costs, volumes):
        self.model.clear()
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
        taxa_co = total_co_pool / base_total_rateio if is_ideal else 0

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