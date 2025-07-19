import json
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                               QLabel, QPushButton, QHBoxLayout, QFrame, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from model.Session import Session
from model.ProductRepository import ProductRepository

class ProductListWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Layout principal que conterá o cabeçalho e a área de rolagem
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # --- Cabeçalho (reutilizado de outras telas) ---
        header_layout = QHBoxLayout()
        
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        
        header_layout.addStretch(1)

        sair_button = QPushButton("Sair")
        sair_button.setObjectName("sair")
        sair_button.clicked.connect(self.logout_and_switch_to_welcome)
        header_layout.addWidget(sair_button)

        self.perfil_label = QLabel()
        self.perfil_label.setObjectName("perfil")
        header_layout.addWidget(self.perfil_label)

        header_container = QWidget()
        header_container.setLayout(header_layout)
        main_layout.addWidget(header_container)

        # --- Linha Divisória ---
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        line1.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 3px;")
        main_layout.addWidget(line1)

        # --- Título ---
        self.title = QLabel("Produtos Cadastrados")
        self.title.setObjectName("pergunta") # Usando o mesmo estilo do formulário
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        # --- Área de Rolagem para o conteúdo principal ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Essencial para o layout interno se ajustar
        scroll_area.setFrameShape(QFrame.NoFrame) # Remove a borda da área de rolagem
        main_layout.addWidget(scroll_area)

        # --- Widget de Conteúdo (que ficará dentro da área de rolagem) ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget) # Layout para o conteúdo
        content_layout.setSpacing(15)

        # Tabela de produtos adicionada ao layout do conteúdo
        self.table = QTableWidget()
        content_layout.addWidget(self.table)

        # Layout para centralizar o botão de atualizar
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.load_products)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch(1)
        content_layout.addLayout(button_layout)

        # Define o widget de conteúdo como o widget da área de rolagem
        scroll_area.setWidget(content_widget)


    def load_products(self):
        user_id = Session().user_id
        if user_id is None:
            self.title.setText("Usuário não está logado.")
            self.table.setRowCount(0) # Limpa a tabela se não houver usuário
            return

        repo = ProductRepository()
        products = repo.get_products_by_user(user_id)
        
        self.title.setText(f"Produtos Cadastrados ({len(products)})")

        self.table.setRowCount(len(products))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Nome", "Data Projeto", "Data Início", "Ativo", "Data Fim", "Preço", "Árvore do Produto"
        ])

        for row_idx, product in enumerate(products):
            self.table.setItem(row_idx, 0, QTableWidgetItem(product.name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(product.dateProject)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(product.dateStart)))
            self.table.setItem(row_idx, 3, QTableWidgetItem("Sim" if product.isActive else "Não"))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(product.endTime) if product.endTime else "N/A"))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"R$ {product.price:.2f}"))
            self.table.setItem(row_idx, 6, QTableWidgetItem(product.productTree))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def update_user_info(self):
        session = Session()
        username_display = session.username if session.username else "Não Conectado"
        self.perfil_label.setText(f"Conectado: {username_display}")

    def logout_and_switch_to_welcome(self):
        Session.user_id = None
        Session.username = None
        self.stacked_widget.setCurrentIndex(0)
    
    def switch_to_welcome(self):
        self.stacked_widget.setCurrentIndex(2)