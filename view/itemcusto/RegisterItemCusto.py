from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QLineEdit, QFrame, QRadioButton,
                               QDoubleSpinBox, QMessageBox, QScrollArea,
                               QFormLayout, QGroupBox, QComboBox)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from model.Session import Session
from model.ItemCusto import ItemCusto  # Importa o modelo correto
from model.ItemCustoRepository import ItemCustoRepository  # Importa o repositório correto

class RegisterItemCustoWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        # Instancia o repositório de Item de Custo
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

        # --- Título (Alterado) ---
        title = QLabel("Cadastro de Itens de Custo")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        # --- Formulário (Adaptado para ItemCusto) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(15)

        self.lbl_id = QLabel("Novo")
        form_layout.addRow("ID:", self.lbl_id)

        self.txt_produto_id = QLineEdit()
        self.txt_produto_id.setPlaceholderText("Código ou nome do produto final")
        form_layout.addRow("Produto ID:", self.txt_produto_id)

        self.txt_descricao = QLineEdit()
        self.txt_descricao.setPlaceholderText("Descrição do insumo ou da atividade")
        form_layout.addRow("Descrição do Item:", self.txt_descricao)

        # Layout horizontal para Quantidade e Medida
        qty_layout = QHBoxLayout()
        self.spin_quantidade = QDoubleSpinBox()
        self.spin_quantidade.setDecimals(4)
        self.spin_quantidade.setMaximum(999999.9999)
        self.combo_medida = QComboBox()
        self.combo_medida.addItems(['Unid', 'ml', 'litros', 'kg', 'kW/h', 'h'])
        qty_layout.addWidget(self.spin_quantidade)
        qty_layout.addWidget(self.combo_medida)
        form_layout.addRow("Quantidade / Medida:", qty_layout)

        self.spin_valor_unitario = QDoubleSpinBox()
        self.spin_valor_unitario.setPrefix("R$ ")
        self.spin_valor_unitario.setDecimals(4)
        self.spin_valor_unitario.setMaximum(999999.9999)
        form_layout.addRow("Valor Unitário:", self.spin_valor_unitario)
        
        # Valor Total (Calculado e somente leitura)
        self.lbl_valor_total = QLabel("R$ 0.00")
        font = QFont()
        font.setBold(True)
        self.lbl_valor_total.setFont(font)
        form_layout.addRow("Valor Total:", self.lbl_valor_total)

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(['MD', 'MOD', 'CIF', 'CO'])
        form_layout.addRow("Categoria:", self.combo_categoria)
        
        # Classificação (Rádio buttons)
        classif_group = QGroupBox("Classificação")
        classif_layout = QHBoxLayout()
        self.radio_variavel = QRadioButton("Variável")
        self.radio_fixo = QRadioButton("Fixo")
        self.radio_variavel.setChecked(True)
        classif_layout.addWidget(self.radio_variavel)
        classif_layout.addWidget(self.radio_fixo)
        classif_group.setLayout(classif_layout)
        form_layout.addRow(classif_group)
        
        # Conectar sinais para cálculo automático
        self.spin_quantidade.valueChanged.connect(self.update_valor_total)
        self.spin_valor_unitario.valueChanged.connect(self.update_valor_total)

        scroll.setWidget(form_container)
        main_layout.addWidget(scroll)

        # --- Botões (Padrão) ---
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar Item")
        btn_salvar.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_salvar.clicked.connect(self.salvar_item_custo)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #f44336; color: white;")
        btn_cancelar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_salvar)
        main_layout.addLayout(btn_layout)

    def update_valor_total(self):
        """Calcula e atualiza o valor total com base na quantidade e valor unitário."""
        quantidade = self.spin_quantidade.value()
        valor_unitario = self.spin_valor_unitario.value()
        total = quantidade * valor_unitario
        self.lbl_valor_total.setText(f"R$ {total:.2f}")

    def logout_and_switch_to_welcome(self):
        Session().clear_session()
        self.stacked_widget.setCurrentIndex(0)

    def update_user_info(self):
        session = Session()
        username = session.username if session.username else "Não conectado"
        self.perfil_label.setText(f"Usuário: {username}")

    def salvar_item_custo(self):
        if not self.txt_produto_id.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe o ID do Produto!")
            return
        if not self.txt_descricao.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe a Descrição do Item!")
            return

        try:
            quantidade = self.spin_quantidade.value()
            valor_unitario = self.spin_valor_unitario.value()
            
            item = ItemCusto(
                produto_id=self.txt_produto_id.text(),
                quantidade=quantidade,
                medida=self.combo_medida.currentText(),
                descricao=self.txt_descricao.text(),
                valor_unitario=valor_unitario,
                valor_total=quantidade * valor_unitario, # Recalcula para garantir
                categoria=self.combo_categoria.currentText(),
                classificacao="Variável" if self.radio_variavel.isChecked() else "Fixo",
                user_id=Session().user_id
            )

            self.item_custo_repo.add_item_custo(item)
            QMessageBox.information(self, "Sucesso", "Item de custo cadastrado com sucesso!")
            self.limpar_formulario()
            self.stacked_widget.setCurrentIndex(1)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao cadastrar o item de custo:\n{str(e)}")

    def limpar_formulario(self):
        """Reseta todos os campos do formulário."""
        self.lbl_id.setText("Novo")
        self.txt_produto_id.clear()
        self.txt_descricao.clear()
        self.spin_quantidade.setValue(0)
        self.combo_medida.setCurrentIndex(0)
        self.spin_valor_unitario.setValue(0)
        self.lbl_valor_total.setText("R$ 0.00")
        self.combo_categoria.setCurrentIndex(0)
        self.radio_variavel.setChecked(True)