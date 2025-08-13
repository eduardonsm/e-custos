from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QLineEdit, QFrame, QRadioButton,
                              QDoubleSpinBox, QSpinBox, QMessageBox, QScrollArea,
                              QFormLayout, QGroupBox, QButtonGroup)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from model.Session import Session
from model.MaterialDireto import MaterialDireto
from model.MaterialDiretoRepository import MaterialDiretoRepository

class RegisterMaterialDiretoWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.material_repo = MaterialDiretoRepository()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Cabeçalho ---
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

        # --- Divisória ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # --- Título ---
        title = QLabel("Cadastro de Materiais Diretos")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        # --- Formulário (Scroll Area) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(15)

        # ID (somente exibição)
        self.lbl_id = QLabel("Novo")
        form_layout.addRow("ID:", self.lbl_id)

        # Descrição
        self.txt_descricao = QLineEdit()
        self.txt_descricao.setPlaceholderText("Descrição do material")
        form_layout.addRow("Descrição:", self.txt_descricao)

        # Fonte (Rádio buttons)
        fonte_group = QGroupBox("Fonte do Material")
        fonte_layout = QHBoxLayout()
        self.radio_fornecido = QRadioButton("Fornecido")
        self.radio_produzido = QRadioButton("Produzido")
        self.radio_fornecido.setChecked(True)
        
        fonte_layout.addWidget(self.radio_fornecido)
        fonte_layout.addWidget(self.radio_produzido)
        fonte_group.setLayout(fonte_layout)
        form_layout.addRow(fonte_group)

        # Lead Times
        self.txt_lead_producao = QLineEdit()
        self.txt_lead_producao.setPlaceholderText("Ex: 15 Dias")
        form_layout.addRow("Lead Time de Produção:", self.txt_lead_producao)

        self.txt_lead_fornecimento = QLineEdit()
        self.txt_lead_fornecimento.setPlaceholderText("Ex: 10 Dias")
        form_layout.addRow("Lead Time de Fornecimento:", self.txt_lead_fornecimento)

        # Fornecedor
        self.txt_fornecedor = QLineEdit()
        self.txt_fornecedor.setPlaceholderText("Nome do fornecedor")
        form_layout.addRow("Fornecedor Atual:", self.txt_fornecedor)

        # Valor Unitário
        self.spin_valor = QDoubleSpinBox()
        self.spin_valor.setPrefix("R$ ")
        self.spin_valor.setDecimals(2)
        self.spin_valor.setMaximum(999999.99)
        form_layout.addRow("Valor Unitário:", self.spin_valor)

        # Estoques
        self.spin_estoque_atual = QSpinBox()
        self.spin_estoque_atual.setMinimum(0)
        self.spin_estoque_atual.setMaximum(999999)
        form_layout.addRow("Estoque Atual:", self.spin_estoque_atual)

        self.spin_estoque_minimo = QSpinBox()
        self.spin_estoque_minimo.setMinimum(0)
        self.spin_estoque_minimo.setMaximum(999999)
        form_layout.addRow("Estoque Mínimo:", self.spin_estoque_minimo)

        self.spin_estoque_maximo = QSpinBox()
        self.spin_estoque_maximo.setMinimum(1)
        self.spin_estoque_maximo.setMaximum(999999)
        form_layout.addRow("Estoque Máximo:", self.spin_estoque_maximo)

        # Conectar sinais para atualizar dinamicamente
        self.radio_fornecido.toggled.connect(self.update_fonte_fields)
        self.radio_produzido.toggled.connect(self.update_fonte_fields)
        self.update_fonte_fields()

        scroll.setWidget(form_container)
        main_layout.addWidget(scroll)

        # --- Botões ---
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar Material")
        btn_salvar.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_salvar.clicked.connect(self.salvar_material)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #f44336; color: white;")
        btn_cancelar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_salvar)
        main_layout.addLayout(btn_layout)

    def update_fonte_fields(self):
        """Atualiza campos habilitados com base na fonte selecionada"""
        produzido = self.radio_produzido.isChecked()
        self.txt_lead_producao.setEnabled(produzido)
        self.txt_lead_fornecimento.setEnabled(not produzido)

    def logout_and_switch_to_welcome(self):
        Session().clear_session()
        self.stacked_widget.setCurrentIndex(0)

    def update_user_info(self):
        session = Session()
        username = session.username if session.username else "Não conectado"
        self.perfil_label.setText(f"Usuário: {username}")

    def salvar_material(self):
        # Validação básica
        if not self.txt_descricao.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe a descrição do material!")
            return

        if not self.txt_fornecedor.text().strip() and not self.radio_produzido.isChecked():
            QMessageBox.warning(self, "Atenção", "Informe o fornecedor para materiais fornecidos!")
            return

        try:
            # Obter dados do formulário
            fonte = "Produzido" if self.radio_produzido.isChecked() else "Fornecido"
            
            material = MaterialDireto(
                descricao=self.txt_descricao.text(),
                fonte=fonte,
                lead_time_producao=self.txt_lead_producao.text() if fonte == "Produzido" else "0 Dias",
                lead_time_fornecimento=self.txt_lead_fornecimento.text() if fonte == "Fornecido" else "0 Dias",
                fornecedor=self.txt_fornecedor.text(),
                valor_unitario=self.spin_valor.value(),
                estoque_atual=self.spin_estoque_atual.value(),
                estoque_minimo=self.spin_estoque_minimo.value(),
                estoque_maximo=self.spin_estoque_maximo.value(),
                user_id=Session().user_id
            )

            # Salvar no banco de dados
            self.material_repo.add_material(material)
            
            QMessageBox.information(self, "Sucesso", "Material cadastrado com sucesso!")
            self.limpar_formulario()
            self.stacked_widget.setCurrentIndex(1)  # Volta para home
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao cadastrar material:\n{str(e)}")

    def limpar_formulario(self):
        """Reseta todos os campos do formulário"""
        self.lbl_id.setText("Novo")
        self.txt_descricao.clear()
        self.radio_fornecido.setChecked(True)
        self.txt_lead_producao.clear()
        self.txt_lead_fornecimento.clear()
        self.txt_fornecedor.clear()
        self.spin_valor.setValue(0)
        self.spin_estoque_atual.setValue(0)
        self.spin_estoque_minimo.setValue(0)
        self.spin_estoque_maximo.setValue(1)