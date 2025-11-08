import collections
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QSplitter, QGridLayout, QFileDialog,
                               QLabel, QPushButton, QGroupBox, QCheckBox, QRadioButton, 
                               QButtonGroup, QDateEdit, QScrollArea, QComboBox, QTableView,
                               QFormLayout, QMessageBox, QSpinBox, QFrame, QSizePolicy, QHBoxLayout)
from PySide6.QtGui import QFont, QImage, QStandardItem, QStandardItemModel, QPainter, QColor, QPageLayout, QPageSize
from PySide6.QtCore import Qt, QDate, QMarginsF, QRectF, QPointF
from PySide6.QtCharts import (QChartView, QChart, QPieSeries, QStackedBarSeries, 
                              QBarSet, QBarCategoryAxis, QValueAxis, QBarSeries)
from PySide6.QtPrintSupport import QPrinter
import io
import matplotlib.pyplot as plt
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

        self.report_data_for_export = None

        self.init_ui()
        self._setup_filter_rules()

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

        selection_and_volumes_layout = QVBoxLayout()
        selection_and_volumes_layout.addWidget(self._create_product_selection_group())
        selection_and_volumes_layout.addWidget(self._create_volumes_group())

        grid_layout.addLayout(selection_and_volumes_layout, 0, 0, 2, 1)
        grid_layout.addWidget(self._create_period_group(), 0, 1)
        grid_layout.addWidget(self._create_category_group(), 0, 2)
        grid_layout.addWidget(self._create_principle_group(), 0, 3)
        grid_layout.addWidget(self._create_cif_rateio_group(), 1, 1)
        grid_layout.addWidget(self._create_classification_group(), 1, 2)
        grid_layout.addWidget(self._create_visualization_group(), 1, 3)
        main_layout.addLayout(grid_layout)

        action_buttons_layout = QHBoxLayout()
        btn_generate = QPushButton("Gerar relatório")
        btn_generate.setFont(QFont("Arial", 12, QFont.Bold))
        btn_generate.setStyleSheet("""
            QPushButton { background-color: #2c3e50; color: white; border-radius: 5px; padding: 10px; }
            QPushButton:hover { background-color: #34495e; }
        """)
        btn_generate.clicked.connect(self.generate_report)

        self.btn_export_pdf = QPushButton("Exportar para PDF")
        self.btn_export_pdf.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_export_pdf.setStyleSheet("""
            QPushButton { background-color: #16a085; color: white; border-radius: 5px; padding: 10px; }
            QPushButton:hover { background-color: #1abc9c; }
            QPushButton:disabled { background-color: #95a5a6; }
        """)
        self.btn_export_pdf.clicked.connect(self.export_to_pdf)
        self.btn_export_pdf.setEnabled(False) # Começa desabilitado

        action_buttons_layout.addStretch()
        action_buttons_layout.addWidget(btn_generate)
        action_buttons_layout.addWidget(self.btn_export_pdf) # Adiciona o novo botão
        action_buttons_layout.addStretch()
        main_layout.addLayout(action_buttons_layout)

        # 1. Crie a área de rolagem para os resultados
        results_scroll_area = QScrollArea()
        results_scroll_area.setWidgetResizable(True) # Essencial para o conteúdo se ajustar!
        results_scroll_area.setFrameShape(QFrame.NoFrame) # Deixa a transição mais suave, sem bordas

        # 2. Crie o splitter vertical como antes
        results_splitter = QSplitter(Qt.Vertical)

        # 3. Crie e adicione a tabela e o gráfico AO SPLITTER (igual antes)
        self.table_report = QTableView()
        self.model = QStandardItemModel()
        self.table_report.setModel(self.model)
        self.table_report.setEditTriggers(QTableView.NoEditTriggers)
        results_splitter.addWidget(self.table_report)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(400)
        results_splitter.addWidget(self.chart_view)

        # Defina tamanhos iniciais para o splitter
        results_splitter.setSizes([300, 600])

        # 4. Coloque o SPLITTER DENTRO da área de rolagem
        results_scroll_area.setWidget(results_splitter)
        results_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 5. Adicione a ÁREA DE ROLAGEM ao layout principal
        main_layout.addWidget(results_scroll_area)

        # Oculta a tabela e o gráfico inicialmente
        self.table_report.setVisible(False)
        self.chart_view.setVisible(False)
    # --- (O resto dos métodos de criação da UI permanecem os mesmos) ---
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
        self.group_volumes = group
        self.group_volumes.setVisible(False)
        return group
    def _create_period_group(self):
        group = QGroupBox("Período (Início e Fim)")
        layout = QVBoxLayout()
        self.date_inicio = QDateEdit(QDate.currentDate().addYears(-5))
        self.date_inicio.setCalendarPopup(True)
        self.date_fim = QDateEdit(QDate.currentDate())
        self.date_fim.setCalendarPopup(True)
        layout.addWidget(QLabel("Início:"))
        layout.addWidget(self.date_inicio)
        layout.addWidget(QLabel("Fim:"))
        layout.addWidget(self.date_fim)
        layout.addStretch()
        group.setLayout(layout)
        return group
    def _create_category_group(self):
        self.group_category = QGroupBox("Categoria")
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
        self.group_category.setLayout(layout)
        return self.group_category
    def _create_classification_group(self):
        self.group_classification = QGroupBox("Classificação")
        layout = QVBoxLayout()
        self.chk_class_fixos = QCheckBox("C. Fixos")
        self.chk_class_variaveis = QCheckBox("C. Variáveis")
        layout.addWidget(self.chk_class_fixos)
        layout.addWidget(self.chk_class_variaveis)
        layout.addStretch()
        self.group_classification.setLayout(layout)
        return self.group_classification
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
        self.chk_viz_graficos.setChecked(True)
        layout.addWidget(self.chk_viz_tabelas)
        layout.addWidget(self.chk_viz_graficos)
        layout.addStretch()
        group.setLayout(layout)
        return group
    def _setup_filter_rules(self):
        all_category_chks = list(self.category_checkboxes.values()) + [self.chk_cat_todos]
        all_class_chks = [self.chk_class_fixos, self.chk_class_variaveis]
        for chk in all_category_chks:
            chk.stateChanged.connect(self._on_category_change)
        for chk in all_class_chks:
            chk.stateChanged.connect(self._on_classification_change)
    def _on_category_change(self):
        is_any_category_checked = any(chk.isChecked() for chk in self.category_checkboxes.values()) or self.chk_cat_todos.isChecked()
        self.group_classification.setEnabled(not is_any_category_checked)
    def _on_classification_change(self):
        is_any_class_checked = self.chk_class_fixos.isChecked() or self.chk_class_variaveis.isChecked()
        self.group_category.setEnabled(not is_any_class_checked)
    def load_data(self):
        self.populate_product_selection()
    def _toggle_all_products(self, state):
        for checkbox in self.product_checkboxes.values():
            if checkbox.text().lower() != "nenhum":
                checkbox.setChecked(bool(state))
    def _toggle_all_categories(self, state):
        for checkbox in self.category_checkboxes.values():
            checkbox.setChecked(bool(state))
    def populate_product_selection(self):
        for i in reversed(range(self.product_selection_layout.count())): 
            self.product_selection_layout.itemAt(i).widget().setParent(None)
        self.product_checkboxes.clear()
        user_id = Session().user_id
        if not user_id: return
        try:
            produtos = self.item_custo_repo.get_distinct_produto_ids(user_id)
            self.chk_todos = QCheckBox("Todos")
            self.chk_todos.stateChanged.connect(self._toggle_all_products)
            self.product_selection_layout.addWidget(self.chk_todos)
            produtos_reais = [p for p in produtos if p.lower() != 'nenhum']
            for pid in produtos_reais:
                chk = QCheckBox(pid)
                self.product_checkboxes[pid] = chk
                self.product_selection_layout.addWidget(chk)
            self.product_selection_layout.addStretch()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível carregar a lista de produtos: {e}")
    def update_volume_inputs(self):
        while self.form_layout_volumes.count():
            self.form_layout_volumes.takeAt(0).widget().deleteLater()
        self.volume_inputs.clear()
        selected_products = [pid for pid, chk in self.product_checkboxes.items() if chk.isChecked()]
        if not selected_products:
            self.group_volumes.setVisible(False)
            return
        for pid in selected_products:
            spin_box = QSpinBox()
            spin_box.setRange(1, 999999)
            spin_box.setValue(100)
            self.form_layout_volumes.addRow(QLabel(f"Volume para {pid}:"), spin_box)
            self.volume_inputs[pid] = spin_box
        self.group_volumes.setVisible(True)

    def generate_report(self):
        # Limpa e exibe as áreas de resultado
        self.table_report.setVisible(self.chk_viz_tabelas.isChecked())
        self.chart_view.setVisible(self.chk_viz_graficos.isChecked())
        self.model.clear()
        self.chart_view.setChart(QChart())
        self.btn_export_pdf.setEnabled(False) # Desabilita o botão ao gerar novo relatório
        self.report_data_for_export = None

        try:
            # Coleta filtros básicos
            user_id = Session().user_id
            if not user_id: return
            
            selected_products = {pid for pid, chk in self.product_checkboxes.items() if chk.isChecked()}
            selected_categories = {cat for cat, chk in self.category_checkboxes.items() if chk.isChecked()}
            if self.chk_cat_todos.isChecked():
                selected_categories.update(self.category_checkboxes.keys())
            
            volumes = {pid: spinbox.value() for pid, spinbox in self.volume_inputs.items()}
            if selected_products and not volumes:
                QMessageBox.warning(self, "Atenção", "Confirme os produtos para definir os volumes antes de gerar o relatório.")
                return

            # --- PREPARAÇÃO CENTRALIZADA DOS DADOS ---
            all_items = self.item_custo_repo.get_itens_by_user(user_id)
            report_data = self._prepare_chart_data(all_items, selected_products, volumes)

            # --- GERAÇÃO DE GRÁFICOS ---
            if self.chk_viz_graficos.isChecked():
                if not selected_categories:
                    QMessageBox.warning(self, "Atenção", "Selecione ao menos uma categoria para gerar o gráfico.")
                    return
                
                # Se nenhum produto selecionado, mostra pizza geral dos custos diretos e indiretos
                if not selected_products:
                    self._gerar_grafico_pizza_geral(all_items, selected_categories)
                # Se um ou mais produtos selecionados, usa os dados com rateio
                elif len(selected_products) == 1:
                    self._gerar_grafico_pizza_produto(report_data, selected_categories)
                else: # 2 ou mais produtos
                    self._gerar_grafico_barras_empilhadas(report_data, selected_categories)

            # --- GERAÇÃO DE TABELAS ---
            if self.chk_viz_tabelas.isChecked():
                # A lógica das tabelas pode ser simplificada no futuro para usar o 'report_data'
                # Por enquanto, mantemos a lógica original para garantir consistência
                itens_overhead = [item for item in all_items if item.produto_id.lower() == 'nenhum']
                itens_produtos = [item for item in all_items if item.produto_id in volumes.keys()]
                product_costs = {pid: {'MD': 0, 'MOD': 0} for pid in volumes.keys()}
                for item in itens_produtos:
                    if item.produto_id in product_costs:
                        if item.categoria == 'MD': product_costs[item.produto_id]['MD'] += item.valor_total
                        elif item.categoria == 'MOD': product_costs[item.produto_id]['MOD'] += item.valor_total
                
                if self.radio_variavel.isChecked():
                    self.gerar_relatorio_variavel(product_costs, volumes)
                else:
                    self.gerar_relatorio_absorcao(product_costs, volumes, itens_overhead)

            self.report_data_for_export = {
                'filters': {
                    'periodo_inicio': self.date_inicio.date().toString("dd/MM/yyyy"),
                    'periodo_fim': self.date_fim.date().toString("dd/MM/yyyy"),
                    'principio': self.principle_group.checkedButton().text(),
                    'produtos': selected_products if selected_products else "Todos"
                }
            }
            self.btn_export_pdf.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Erro no Cálculo", f"Ocorreu um erro ao gerar o relatório: {e}")
    def _create_bar_chart_image(self, report_data, selected_categories):
        """
        Cria a imagem do gráfico de barras com labels inteligentes:
        - Dentro da barra para valores grandes.
        - Fora da barra para valores pequenos.
        """
        selected_products = list(report_data.keys())
        product_totals = [sum(report_data[prod].values()) for prod in selected_products]

        fig, ax = plt.subplots(figsize=(11, 7)) # Aumentei a figura para dar mais espaço

        bottoms = [0] * len(selected_products)
        
        for category in selected_categories:
            values = [report_data[prod].get(category, 0) for prod in selected_products]
            ax.bar(selected_products, values, label=category, bottom=bottoms)

            # --- NOVA LÓGICA DE LABELS INTELIGENTES ---
            for i, (value, bottom_val) in enumerate(zip(values, bottoms)):
                total_da_barra = product_totals[i]
                
                if total_da_barra == 0 or value == 0:
                    continue

                percentage = (value / total_da_barra) * 100
                label_text = f"{percentage:.1f}%"

                # Se o segmento for grande, o label vai dentro.
                if percentage > 4:
                    y_pos = bottom_val + value / 2
                    ax.text(i, y_pos, label_text, ha='center', va='center', color='white', weight='bold', fontsize=9)
                # Se o segmento for pequeno, o label vai fora.
                else:
                    y_pos = bottom_val + value # Posição no topo do segmento
                    # Desenha o texto um pouco acima da barra
                    ax.text(i, y_pos + (total_da_barra * 0.01), label_text, ha='center', va='bottom', color='black', fontsize=8)
            
            # Atualiza a base para a próxima categoria
            for i, value in enumerate(values):
                bottoms[i] += value

        ax.set_title('Comparativo de Custos por Produto e Categoria', fontsize=16, weight='bold', pad=20)
        ax.set_ylabel('Custo Total (R$)', fontsize=12)
        ax.set_xticks(range(len(selected_products)))
        ax.set_xticklabels(selected_products, rotation=15, ha='right')
        ax.legend(title='Categorias', bbox_to_anchor=(1.02, 1), loc='upper left')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter('R$ {:,.0f}'.format)

        # Aumenta o limite do eixo Y para garantir que os labels externos caibam
        if product_totals:
            ax.set_ylim(top=max(product_totals) * 1.20)

        fig.tight_layout(rect=[0, 0, 0.88, 1]) # Ajusta o layout para dar espaço à legenda

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        plt.close(fig)
        return buf
    def _create_pie_chart_image(self, report_data, selected_categories):
        """Cria uma imagem de alta qualidade do gráfico de pizza em memória."""
        product_id = list(report_data.keys())[0]
        costs = report_data[product_id]

        # Filtra apenas as categorias selecionadas e com valor > 0
        labels = [cat for cat in selected_categories if costs.get(cat, 0) > 0]
        sizes = [costs[cat] for cat in labels]

        if not sizes: return None

        fig, ax = plt.subplots(figsize=(8, 6))

        def func(pct, allvals):
            absolute = int(round(pct/100.*sum(allvals)))
            return f"{pct:.1f}%\n(R$ {absolute:,.0f})"

        ax.pie(sizes, labels=labels, autopct=lambda pct: func(pct, sizes), startangle=90, wedgeprops=dict(width=0.4))
        ax.set_title(f"Composição de Custos para: {product_id}", fontsize=14, weight='bold')
        ax.axis('equal') # Garante que a pizza seja um círculo

        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        plt.close(fig)
        return buf
    def export_to_pdf(self):
        if not self.report_data_for_export:
            QMessageBox.warning(self, "Atenção", "Gere um relatório antes de exportar.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_path)
        printer.setPageLayout(QPageLayout(QPageSize.A4, QPageLayout.Portrait, QMarginsF(20, 20, 20, 20)))

        painter = QPainter(printer)
        
        font_titulo = QFont("Arial", 16, QFont.Bold)
        font_subtitulo = QFont("Arial", 12, QFont.Bold)
        font_normal = QFont("Arial", 10)
        
        rect = painter.viewport()
        y_cursor = 20.0 # Começa com a margem

        # --- DESENHA O CABEÇALHO ---
        painter.setFont(font_titulo)
        painter.drawText(QRectF(0, y_cursor, rect.width(), 40), Qt.AlignHCenter, "Relatório de Custos - e-Custos")
        y_cursor += 60
        
        painter.setFont(font_subtitulo)
        painter.drawText(QPointF(20, y_cursor), "Filtros Utilizados")
        y_cursor += 25
        
        painter.setFont(font_normal)
        filters = self.report_data_for_export['filters']
        produtos_str = ", ".join(filters['produtos']) if filters['produtos'] != 'Todos' else 'Todos'
        filter_text = (
            f"Período: {filters['periodo_inicio']} a {filters['periodo_fim']}\n"
            f"Princípio de Custeio: {filters['principio']}\n"
            f"Produtos: {produtos_str}"
        )
        
        # CORREÇÃO 2: Usa boundingRect para calcular a altura real do texto
        filter_rect = QRectF(20, y_cursor, rect.width() - 40, 150)
        bounding_rect = painter.boundingRect(filter_rect, Qt.AlignLeft, filter_text)
        painter.drawText(filter_rect, Qt.AlignLeft, filter_text)
        y_cursor += bounding_rect.height() + 20 # Avança o cursor pela altura real do texto + espaçamento

        # --- DESENHA O GRÁFICO ---
        if self.chart_view.isVisible():
            painter.setFont(font_subtitulo)
            painter.drawText(QPointF(20, y_cursor), "Gráfico de Custos")
            y_cursor += 30
            
            all_items = self.item_custo_repo.get_itens_by_user(Session().user_id)
            selected_products = self.report_data_for_export['filters']['produtos']
            selected_categories = {cat for cat, chk in self.category_checkboxes.items() if chk.isChecked()}
            if self.chk_cat_todos.isChecked(): selected_categories.update(self.category_checkboxes.keys())
            
            volumes = {pid: spinbox.value() for pid, spinbox in self.volume_inputs.items()}
            report_data = self._prepare_chart_data(all_items, selected_products, volumes)

            chart_buffer = None
            if len(selected_products) > 1 or self.chk_todos.isChecked():
                chart_buffer = self._create_bar_chart_image(report_data, selected_categories)
            elif len(selected_products) == 1:
                chart_buffer = self._create_pie_chart_image(report_data, selected_categories)

            # Desenha a imagem gerada no PDF
            if chart_buffer:
                chart_image = QImage.fromData(chart_buffer.read())
                # Define uma área grande e de alta qualidade para o gráfico
                chart_height = (rect.width() - 40) * chart_image.height() / chart_image.width()
                chart_rect = QRectF(20, y_cursor, rect.width() - 40, chart_height)
                painter.drawImage(chart_rect, chart_image)
                y_cursor += chart_height + 20
        printer.newPage()
        y_cursor = 20
        # --- DESENHA A TABELA ---
        if self.table_report.isVisible():
            y_cursor += 20
            painter.setFont(font_subtitulo)
            painter.drawText(QPointF(20, y_cursor), "Detalhamento de Custos")
            y_cursor += 30

            # GERA A IMAGEM DA TABELA USANDO A NOVA FUNÇÃO
            table_buffer = self._create_table_image(self.model)

            if table_buffer:
                table_image = QImage.fromData(table_buffer.read())
                # Redimensiona a imagem da tabela para caber na largura da página
                table_height = (rect.width() - 40) * table_image.height() / table_image.width()
                
                # Se a tabela for muito alta, passa para a próxima página
                if y_cursor + table_height > rect.height() - 20:
                    printer.newPage()
                    y_cursor = 20

                table_rect = QRectF(20, y_cursor, rect.width() - 40, table_height)
                painter.drawImage(table_rect, table_image)
            
            # painter.restore()
        
        painter.end()
        QMessageBox.information(self, "Sucesso", f"Relatório salvo com sucesso em:\n{file_path}")
    def _create_table_image(self, model):
        """Cria uma imagem de alta qualidade da tabela de dados em memória usando Matplotlib."""
        if model.rowCount() == 0 or model.columnCount() == 0:
            return None

        # Extrai os dados do modelo da tabela do Qt
        headers = [model.headerData(c, Qt.Horizontal) for c in range(model.columnCount())]
        cell_data = []
        for r in range(model.rowCount()):
            row_data = [model.item(r, c).text() for c in range(model.columnCount())]
            cell_data.append(row_data)

        # Estima a altura necessária para a figura
        # Ajuste o valor 0.3 se as linhas ficarem muito apertadas ou espaçadas
        fig_height = (len(cell_data) + 1) * 0.3 
        fig, ax = plt.subplots(figsize=(10, fig_height))
        ax.axis('off') # Remove os eixos do gráfico (x, y)

        # Cria a tabela do Matplotlib
        mpl_table = ax.table(cellText=cell_data, colLabels=headers, loc='center', cellLoc='center')

        # --- ESTILIZAÇÃO DA TABELA ---
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(10)
        mpl_table.scale(1.2, 1.2) # Aumenta o tamanho geral da tabela

        for (row, col), cell in mpl_table.get_celld().items():
            # Estiliza o cabeçalho
            if row == 0:
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#2c3e50') # Azul escuro
            # Estiliza as linhas de dados
            else:
                cell.set_facecolor('white')
            
            # Adiciona bordas
            cell.set_edgecolor('grey')

        # Salva a imagem em um buffer de memória
        buf = io.BytesIO()
        # bbox_inches='tight' remove o excesso de margem branca
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0.05)
        buf.seek(0)
        plt.close(fig) # Fecha a figura para liberar memória
        return buf

    def _prepare_chart_data(self, all_items, selected_products, volumes):
        # 1. Inicia com os custos diretos de cada produto
        costs_data = {p: collections.defaultdict(float) for p in selected_products}
        for item in all_items:
            if item.produto_id in costs_data and item.categoria in ['MD', 'MOD']:
                costs_data[item.produto_id][item.categoria] += item.valor_total

        # 2. Se o custeio for por absorção, calcula e adiciona o rateio
        if self.radio_integral.isChecked() or self.radio_ideal.isChecked():
            criterio = self.combo_cif_criterio.currentText()
            is_ideal = self.radio_ideal.isChecked()
            
            # Pools de custos indiretos
            itens_overhead = [item for item in all_items if item.produto_id.lower() == 'nenhum']
            total_cif_pool = sum(item.valor_total for item in itens_overhead if item.categoria == 'CIF')
            total_co_pool = sum(item.valor_total for item in itens_overhead if item.categoria == 'CO') if is_ideal else 0

            # Base total de rateio
            base_total_rateio = 0
            if criterio == "Mão de Obra Direta (MOD)":
                base_total_rateio = sum(costs_data[pid]['MOD'] for pid in selected_products)
            elif criterio == "Material Direto (MD)":
                base_total_rateio = sum(costs_data[pid]['MD'] for pid in selected_products)
            elif criterio == "Volume Produzido":
                base_total_rateio = sum(volumes.values())
            elif criterio == "MOD + MD":
                base_total_rateio = sum(costs_data[pid]['MOD'] + costs_data[pid]['MD'] for pid in selected_products)
            
            if base_total_rateio > 0:
                taxa_cif = total_cif_pool / base_total_rateio
                taxa_co = total_co_pool / base_total_rateio
                
                # Adiciona os custos rateados a cada produto
                for pid in selected_products:
                    base_produto = 0
                    if criterio == "Mão de Obra Direta (MOD)": base_produto = costs_data[pid]['MOD']
                    elif criterio == "Material Direto (MD)": base_produto = costs_data[pid]['MD']
                    elif criterio == "Volume Produzido": base_produto = volumes.get(pid, 0)
                    elif criterio == "MOD + MD": base_produto = costs_data[pid]['MOD'] + costs_data[pid]['MD']
                    
                    costs_data[pid]['CIF'] += base_produto * taxa_cif
                    if is_ideal:
                        costs_data[pid]['CO'] += base_produto * taxa_co
        
        return costs_data
    def _gerar_grafico_pizza_geral(self, all_items, selected_categories):
        # Esta função permanece a mesma, pois mostra o total da empresa
        costs_by_category = collections.defaultdict(float)
        for item in all_items:
            if item.categoria in selected_categories:
                costs_by_category[item.categoria] += item.valor_total
        total_cost = sum(costs_by_category.values())
        if total_cost == 0: return
        series = QPieSeries()
        for category, cost in costs_by_category.items():
            percentage = (cost / total_cost) * 100
            slice_ = series.append(f"{category} ({percentage:.1f}%)", cost)
            slice_.setLabelVisible()
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Composição Geral de Custos por Categoria")
        chart.legend().setAlignment(Qt.AlignRight)
        self.chart_view.setChart(chart)
    def _gerar_grafico_pizza_produto(self, report_data, selected_categories):
        # Modificado para receber os dados já calculados (com rateio)
        product_id = list(report_data.keys())[0]
        costs_by_category = report_data[product_id]
        
        total_cost = sum(costs_by_category.values())
        if total_cost == 0: return
        
        series = QPieSeries()
        for category, cost in costs_by_category.items():
            if category in selected_categories and cost > 0:
                percentage = (cost / total_cost) * 100
                slice_ = series.append(f"{category} ({percentage:.1f}%)", cost)
                slice_.setLabelVisible()
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(f"Composição de Custos para: {product_id}")
        chart.legend().setAlignment(Qt.AlignRight)
        self.chart_view.setChart(chart)

        # Dentro da classe PersonalizaRelatorioWindow
    def _gerar_grafico_barras_empilhadas(self, report_data, selected_categories):
        """
        Gera o gráfico de barras empilhadas com um label de TOTAL no topo de cada barra.
        """
        selected_products = list(report_data.keys())
        chart = QChart()
        chart.setTitle("Comparativo de Custos por Produto e Categoria")

        # --- SÉRIE 1: As barras empilhadas e coloridas (sem labels) ---
        series = QStackedBarSeries()
        series.setLabelsVisible(True)
        bar_sets = {cat: QBarSet(cat) for cat in selected_categories}
        for bar_set in bar_sets.values():
            bar_set.setLabelColor(QColor("black"))
        for product in selected_products:
            for category in selected_categories:
                cost = report_data[product].get(category, 0)
                bar_sets[category].append(cost)
                
        
        for bar_set in bar_sets.values():
            series.append(bar_set)
            

        chart.addSeries(series)

        # --- CÁLCULO DOS TOTAIS DE CADA BARRA ---
        product_totals = []
        for product in selected_products:
            total = sum(report_data[product].values())
            product_totals.append(total)

        # --- SÉRIE 2: Uma série invisível apenas para os LABELS de total ---
        label_series = QBarSeries()
        total_set = QBarSet("") # Label vazio para não aparecer na legenda
        total_set.append(product_totals)
        
        # Torna as barras desta série invisíveis
        total_set.setBrush(QColor(Qt.transparent))
        total_set.setPen(QColor(Qt.transparent))
        
        label_series.append(total_set)
        
        # Configura os labels para esta série
        label_series.setLabelsVisible(True)
        label_series.setLabelsPosition(QBarSeries.LabelsOutsideEnd) # Posição: no topo, fora da barra
        label_series.setLabelsFormat("R$ @value") # Formato do texto
        
        chart.addSeries(label_series)

        # --- CONFIGURAÇÃO DOS EIXOS ---
        axis_x = QBarCategoryAxis()
        axis_x.append(selected_products)
        chart.addAxis(axis_x, Qt.AlignBottom)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("R$ %.0f")
        if product_totals:
            axis_y.setMax(max(product_totals) * 1.15) 
            
        chart.addAxis(axis_y, Qt.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        label_series.attachAxis(axis_x)
        label_series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view.setChart(chart)

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