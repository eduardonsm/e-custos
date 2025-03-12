from PySide6.QtWidgets import QFrame, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
import sqlite3
from PySide6.QtCore import Qt
from model.UserRepository import UserRepository

class LoginWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Bem-vindo ao Sistema de Login")

        input_container = QFrame()
        input_container.setObjectName("loginFrame")
        input_layout = QVBoxLayout(input_container)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_input)

        self.login_button = QPushButton("Entrar")
        self.register_button = QPushButton("Registrar")
        
        self.login_button.clicked.connect(self.authenticate_user)
        self.register_button.clicked.connect(self.switch_to_register)
        
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(input_container)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        
        self.setLayout(layout)

    def authenticate_user(self):
      
        if UserRepository.authenticate_user(self):
            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos!")
    
    def switch_to_register(self):
        self.stacked_widget.setCurrentIndex(1)
