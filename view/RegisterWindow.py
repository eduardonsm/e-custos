from PySide6.QtWidgets import QFrame, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
import sqlite3
from PySide6.QtCore import Qt
from model.UserRepository import UserRepository
class RegisterWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.user_repo = UserRepository()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Crie sua Conta")

        input_container = QFrame()
        input_container.setObjectName("loginFrame")
        input_layout = QVBoxLayout(input_container)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.email_input)
        input_layout.addWidget(self.password_input)
        
        self.register_button = QPushButton("Registrar")
        self.back_button = QPushButton("Voltar")
        
        self.register_button.clicked.connect(self.register_user)
        self.back_button.clicked.connect(self.switch_to_login)
        
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(input_container)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def register_user(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos!")
            return
        
        if self.user_repo.add_user(username, email, password):
            QMessageBox.information(self, "Sucesso", "Usuário registrado com sucesso!")
            self.switch_to_login()
        else:
            QMessageBox.warning(self, "Erro", "Nome de usuário ou email já cadastrados!")
    
    def switch_to_login(self):
        self.stacked_widget.setCurrentIndex(0)
