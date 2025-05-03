from PySide6.QtWidgets import QFrame, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
import sqlite3
from PySide6.QtCore import Qt
class Welcome(QWidget):
    """
    Tela de boas-vindas do sistema de login.
    """

    def __init__(self, stacked_widget):
            super().__init__()

            layout = QVBoxLayout()
            #boas vindas
            bemvindo = QLabel("Seja bem-vindo ao aplicativo!")
            layout.addWidget(bemvindo, alignment=Qt.AlignmentFlag.AlignRight)
            titulo = QLabel("Se você já sabe qual princípio e qual método utilizar, favor seleciona-los. Se não, clique no Guia $mart!")
            layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
            #principio e metodo
            principio = QLabel("Princípio:")
            metodo = QLabel("Método:")
            #botao de guia
            guia = QPushButton("Guia $mart")
            guia.setObjectName("guia")
            guia.setStyleSheet("background-color: #4CAF50; color: red;")
            guia.setFixedSize(100, 30)

            # guia.clicked.connect(self.show_guide)

            #botao de sair
            sair = QPushButton("Sair")
            sair.setObjectName("sair")
            sair.setStyleSheet("background-color: #f44336; color: white;")
            sair.setFixedSize(100, 30)
            # sair.clicked.connect(self.close)
            
            #botao de voltar
            voltar = QPushButton("Voltar")
            voltar.setObjectName("voltar")
            voltar.setStyleSheet("background-color: #2196F3; color: white;")
            voltar.setFixedSize(100, 30)
            # voltar.clicked.connect(self.voltar_login)
           
            #botao de proximo
            proximo = QPushButton("Próximo")
            proximo.setObjectName("proximo")
            proximo.setStyleSheet("background-color: #2196F3; color: white;")
            proximo.setFixedSize(100, 30)
            # proximo.clicked.connect(self.proximo)

            #adicionando os botoes ao layout
            layout.addWidget(principio, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(metodo, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(guia, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(sair, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(voltar, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(proximo, alignment=Qt.AlignmentFlag.AlignLeft)
            #adicionando o layout ao widget
            self.setLayout(layout)