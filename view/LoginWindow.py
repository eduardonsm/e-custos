from PySide6.QtWidgets import QFrame, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
import sqlite3
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from model.UserRepository import UserRepository

class LoginWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        mensagem = QLabel("Entre ou Cadastre-se")
        mensagem.setObjectName("pergunta")

        input_container = QFrame()
        input_container.setObjectName("loginFrame")
        input_layout = QVBoxLayout(input_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")
        self.username_input.setMinimumWidth(800)
        self.username_input.setMaximumWidth(800)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setMinimumWidth(800)
        self.password_input.setMaximumWidth(800)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_input)
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_container.setMaximumWidth(900)

        self.login_button = QPushButton("Entrar")
        self.login_button.setFixedWidth(800)
        self.register_button = QPushButton("Registrar")
        self.register_button.setFixedWidth(800)
        
        self.login_button.clicked.connect(self.authenticate_user)
        self.register_button.clicked.connect(self.switch_to_register)
        
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mensagem, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(input_container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def authenticate_user(self):
      
        if UserRepository.authenticate_user(self):
            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
            self.stacked_widget.setCurrentIndex(2)  
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos!")
    
    def switch_to_register(self):
        self.stacked_widget.setCurrentIndex(1)
