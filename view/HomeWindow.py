from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QIcon, QPixmap
from components.CustomRadioButton import CustomRadioButton
from model.Session import Session # Assumindo que Session está em model/Session.py
from PySide6.QtCore import Qt

class HomeWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        main_layout = QVBoxLayout() 

        # --- Cabeçalho ---
        header_layout = QHBoxLayout() 
        
        # Ícone à esquerda
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        
        header_layout.addStretch(1) 
        
        gerar_relatorio = QPushButton("Gerar Relatório")
        gerar_relatorio.setObjectName("gerar_relatorio")
        header_layout.addWidget(gerar_relatorio)

        sair = QPushButton("Sair")
        sair.setObjectName("sair")
        sair.clicked.connect(self.switch_to_login)
        header_layout.addWidget(sair)

        self.perfil = QLabel()
        self.perfil.setObjectName("perfil")
        header_layout.addWidget(self.perfil)
        
        header_container = QWidget()
        header_container.setLayout(header_layout)

        main_layout.addWidget(header_container)

        # --- Conteúdo Principal ---
        content_layout = QVBoxLayout()
        cadastrar = QPushButton("Cadastrar custo")
        cadastrar.setObjectName("cadastrar")
        cadastrar.clicked.connect(self.cadastrar_custo)
        content_layout.addWidget(cadastrar)
        
        # --- cadastrar Produtos ---
        cadastrar_produto = QPushButton("Cadastrar produto")
        cadastrar_produto.setObjectName("cadastrar_produto")
        cadastrar_produto.clicked.connect(self.cadastrar_produto)
        content_layout.addWidget(cadastrar_produto)
        # --- Listar Produtos ---
        listar_produto = QPushButton("Listar produto")
        listar_produto.setObjectName("listar_produto")
        listar_produto.clicked.connect(self.listar_produtos)
        content_layout.addWidget(listar_produto)

        main_layout.addLayout(content_layout)
        main_layout.addStretch(1)

        # --- Configurações Finais da Janela ---
        main_layout.setContentsMargins(20, 20, 20, 20) 
        main_layout.setSpacing(10) 
        self.setLayout(main_layout)

    def switch_to_login(self):
        # Função para mudar para a tela de login
        self.stacked_widget.setCurrentIndex(0)
    def update_user_info(self):
        session = Session()
        username_display = session.username if session.username is not None else "Não Conectado"
        self.perfil.setText(f"Conectado: {username_display}")
    def cadastrar_custo(self):
        home_screen = self.stacked_widget.widget(30)
        home_screen.update_user_info()
        self.stacked_widget.setCurrentIndex(30)
    def cadastrar_produto(self):
        home_screen = self.stacked_widget.widget(31)
        home_screen.update_user_info()
        self.stacked_widget.setCurrentIndex(31)
    def listar_produtos(self):
        listProduct = self.stacked_widget.widget(32)
        listProduct.update_user_info()
        listProduct.load_products()
        self.stacked_widget.setCurrentIndex(32)
        