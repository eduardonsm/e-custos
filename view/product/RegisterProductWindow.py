import json
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, 
                              QLabel, QPushButton, QButtonGroup, QLineEdit, QComboBox, 
                              QSpinBox, QMessageBox, QScrollArea, QFormLayout, QGroupBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from model.Session import Session
from model.Product import Product
from model.ProductRepository import ProductRepository

class RegisterProductWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.product_repo = ProductRepository()
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
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(29))  # Assumindo que 1 é a home
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
        title = QLabel("Cadastro de Produto")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # --- Formulário (Scroll Area) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)

        # ID (somente exibição)
        self.lbl_id = QLabel("Novo")
        form_layout.addRow("ID:", self.lbl_id)

        # Descrição
        self.txt_descricao = QLineEdit()
        self.txt_descricao.setPlaceholderText("Descrição do produto")
        form_layout.addRow("Descrição:", self.txt_descricao)

        # Unidade de Medida
        self.cb_unidade = QComboBox()
        self.cb_unidade.addItems(["UN", "KG", "LT", "MT", "PC"])
        form_layout.addRow("Unidade de Medida:", self.cb_unidade)

        # Categoria
        self.cb_categoria = QComboBox()
        self.cb_categoria.addItems(Product.CATEGORIES)
        form_layout.addRow("Categoria:", self.cb_categoria)

        # Status
        status_group = QGroupBox("Status")
        status_layout = QHBoxLayout()
        self.radio_ativo = QRadioButton("Ativo")
        self.radio_inativo = QRadioButton("Inativo")
        self.radio_desenvolvimento = QRadioButton("Em desenvolvimento")
        self.radio_ativo.setChecked(True)
        
        status_layout.addWidget(self.radio_ativo)
        status_layout.addWidget(self.radio_inativo)
        status_layout.addWidget(self.radio_desenvolvimento)
        status_group.setLayout(status_layout)
        form_layout.addRow(status_group)

        # Centros Produtivos
        self.spin_centros = QSpinBox()
        self.spin_centros.setMinimum(1)
        self.spin_centros.setMaximum(100)
        form_layout.addRow("Quantidade de centros produtivos:", self.spin_centros)

        # Fluxo de Produção
        self.txt_fluxo = QLineEdit()
        self.txt_fluxo.setPlaceholderText("Descreva o fluxo de produção")
        form_layout.addRow("Fluxo de produção:", self.txt_fluxo)

        scroll.setWidget(form_container)
        main_layout.addWidget(scroll)

        # --- Botões ---
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.salvar_produto)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(29))  # Volta para home
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_salvar)
        main_layout.addLayout(btn_layout)

    def logout_and_switch_to_welcome(self):
        Session().clear_session()
        self.stacked_widget.setCurrentIndex(0)

    def update_user_info(self):
        session = Session()
        username = session.username if session.username else "Não conectado"
        self.perfil_label.setText(f"Usuário: {username}")

    def salvar_produto(self):
        # Validação básica
        if not self.txt_descricao.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe a descrição do produto!")
            return

        try:
            # Obter dados do formulário
            product = Product(
                description=self.txt_descricao.text(),
                unit=self.cb_unidade.currentText(),
                category=self.cb_categoria.currentText(),
                status=self.get_selected_status(),
                production_centers=self.spin_centros.value(),
                production_flow=self.txt_fluxo.text(),
                user_id=Session().user_id
            )

            # Salvar no banco de dados
            self.product_repo.add_product(product)
            
            QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso!")
            self.stacked_widget.setCurrentIndex(29)  # Volta para home
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao cadastrar produto:\n{str(e)}")

    def get_selected_status(self):
        if self.radio_ativo.isChecked():
            return "Ativo"
        elif self.radio_inativo.isChecked():
            return "Inativo"
        else:
            return "Em desenvolvimento"