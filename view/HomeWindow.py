from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QIcon, QPixmap
from components.CustomRadioButton import CustomRadioButton
from model.Session import Session # Assumindo que Session está em model/Session.py
import sqlite3

from PySide6.QtCore import Qt

class HomeWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        main_layout = QVBoxLayout() # Renomeado para evitar confusão com 'layout' interno

        # --- Cabeçalho ---
        header_layout = QHBoxLayout() # Layout específico para o cabeçalho
        
        # Ícone à esquerda
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        
        # Espaçador para empurrar os elementos para a direita
        header_layout.addStretch(1) # Este stretch empurra tudo à direita dele para a direita
        
        # Botões e informações do usuário à direita
        gerar_relatorio = QPushButton("Gerar Relatório")
        gerar_relatorio.setObjectName("gerar_relatorio")
        header_layout.addWidget(gerar_relatorio)

        sair = QPushButton("Sair")
        sair.setObjectName("sair")
        sair.clicked.connect(self.switch_to_welcome)
        header_layout.addWidget(sair)

        # Usamos Session.user_id ou um placeholder se for None
        # Idealmente, Session.user_id deve ser definido após o login
        

        self.perfil = QLabel()
        self.perfil.setObjectName("perfil")
        header_layout.addWidget(self.perfil)
        
        # Container para o cabeçalho e suas margens
        header_container = QWidget()
        header_container.setLayout(header_layout)
        # Ajuste as margens do container do cabeçalho se desejar, 
        # mas o addStretch deve resolver a distribuição.
        # header_container.setContentsMargins(0, 0, 0, 0) # Exemplo de como zerar se precisar

        main_layout.addWidget(header_container)

        # --- Conteúdo Principal (que virá abaixo do cabeçalho) ---
        # Adicione aqui outros elementos da sua HomeWindow
        # Por exemplo, um QLabel centralizado para mostrar que a página está em construção:
        # main_layout.addWidget(QLabel("Conteúdo principal da Home Window aqui"), alignment=Qt.AlignCenter)
        
        # Adiciona um stretch no final para empurrar o cabeçalho para o topo
        main_layout.addStretch(1) 

        # --- Configurações Finais da Janela ---
        main_layout.setContentsMargins(20, 20, 20, 20) # Margens internas da janela como um todo
        main_layout.setSpacing(10) # Espaçamento entre os widgets no layout principal
        self.setLayout(main_layout)

    def switch_to_welcome(self):
        # Função para mudar para a tela de seleção
        self.stacked_widget.setCurrentIndex(2)
    def update_user_info(self):
        session = Session()
        username_display = session.username if session.username is not None else "Não Conectado"
        self.perfil.setText(f"Conectado: {username_display}")