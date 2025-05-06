import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon
from view.LoginWindow import LoginWindow
from view.RegisterWindow import RegisterWindow
from view.WelcomeWindow import Welcome
from view.guiasmart.GuiaWindow import GuiaWindow
from view.guiasmart.Pergunta1Window import Pergunta1Window
from view.guiasmart.Pergunta2Window import Pergunta2Window
from view.guiasmart.Pergunta3Window import Pergunta3Window
from view.guiasmart.Pergunta4Window import Pergunta4Window


# Configuração do banco de dados
def create_db():
    conn = sqlite3.connect("model/LoginSystem.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """)
    conn.commit()
    conn.close()


def load_stylesheet(app, file_name="style.qss"):
        try:
            with open(file_name, "r") as file:
                app.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Arquivo de estilo não encontrado. Certifique-se de que 'style.qss' está no mesmo diretório.")


# Aplicação principal
class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        
        self.login_window = LoginWindow(self.stacked_widget)
        self.register_window = RegisterWindow(self.stacked_widget)
        self.welcome_page = Welcome(self.stacked_widget)
        self.guia_window = GuiaWindow(self.stacked_widget)
        self.pergunta1_window = Pergunta1Window(self.stacked_widget)
        self.pergunta2_window = Pergunta2Window(self.stacked_widget)
        self.pergunta3_window = Pergunta3Window(self.stacked_widget)
        self.pergunta4_window = Pergunta4Window(self.stacked_widget)

        
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.register_window)
        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.guia_window)
        self.stacked_widget.addWidget(self.pergunta1_window)
        self.stacked_widget.addWidget(self.pergunta2_window)
        self.stacked_widget.addWidget(self.pergunta3_window)
        self.stacked_widget.addWidget(self.pergunta4_window)
        
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        
        self.setWindowTitle("E-CUSTO$")
        self.setWindowIcon(QIcon("./images/cifrao.png"))
        self.setGeometry(50, 50, 400, 400)

    def showEvent(self, event):
        self.setMinimumSize(1100, 720)  # Tamanho mínimo
        super().showEvent(event)

# Execução da aplicação
if __name__ == "__main__":
    create_db()
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())
