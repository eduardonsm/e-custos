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
from view.guiasmart.Pergunta7Window import Pergunta7Window
from view.guiasmart.Pergunta8Window import Pergunta8Window
from view.guiasmart.Pergunta9Window import Pergunta9Window
from view.guiasmart.Pergunta10Window import Pergunta10Window
from view.guiasmart.Pergunta11Window import Pergunta11Window
from view.guiasmart.Pergunta12Window import Pergunta12Window
from view.guiasmart.Pergunta13Window import Pergunta13Window
from view.guiasmart.Pergunta14Window import Pergunta14Window
from view.guiasmart.Pergunta15Window import Pergunta15Window
from view.guiasmart.Pergunta16Window import Pergunta16Window
from view.guiasmart.Pergunta17Window import Pergunta17Window
from view.guiasmart.Pergunta18Window import Pergunta18Window
from view.guiasmart.Pergunta19Window import Pergunta19Window
from view.guiasmart.Pergunta20Window import Pergunta20Window
from view.guiasmart.Pergunta21Window import Pergunta21Window
from view.guiasmart.Pergunta22Window import Pergunta22Window
from view.guiasmart.Pergunta23Window import Pergunta23Window
from view.guiasmart.Pergunta24Window import Pergunta24Window
from view.guiasmart.Pergunta25Window import Pergunta25Window
from view.guiasmart.Pergunta26Window import Pergunta26Window
from view.guiasmart.Pergunta27Window import Pergunta27Window
from view.guiasmart.Resultado import Resultado
from view.HomeWindow import HomeWindow

# Configuração do banco de dados
def create_db():
    conn = sqlite3.connect("model/LoginSystem.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
         email TEXT NOT NULL UNIQUE,
        metodo TEXT,
        principio TEXT
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
        self.pergunta7_window = Pergunta7Window(self.stacked_widget)
        self.pergunta8_window = Pergunta8Window(self.stacked_widget)
        self.pergunta9_window = Pergunta9Window(self.stacked_widget)
        self.pergunta10_window = Pergunta10Window(self.stacked_widget)
        self.pergunta11_window = Pergunta11Window(self.stacked_widget)
        self.pergunta12_window = Pergunta12Window(self.stacked_widget)
        self.pergunta13_window = Pergunta13Window(self.stacked_widget)
        self.pergunta14_window = Pergunta14Window(self.stacked_widget)
        self.pergunta15_window = Pergunta15Window(self.stacked_widget)
        self.pergunta16_window = Pergunta16Window(self.stacked_widget)
        self.pergunta17_window = Pergunta17Window(self.stacked_widget)
        self.pergunta18_window = Pergunta18Window(self.stacked_widget)
        self.pergunta19_window = Pergunta19Window(self.stacked_widget)
        self.pergunta20_window = Pergunta20Window(self.stacked_widget)
        self.pergunta21_window = Pergunta21Window(self.stacked_widget)
        self.pergunta22_window = Pergunta22Window(self.stacked_widget)
        self.pergunta23_window = Pergunta23Window(self.stacked_widget)
        self.pergunta24_window = Pergunta24Window(self.stacked_widget)
        self.pergunta25_window = Pergunta25Window(self.stacked_widget)
        self.pergunta26_window = Pergunta26Window(self.stacked_widget)
        self.pergunta27_window = Pergunta27Window(self.stacked_widget)
        self.resultado_window = Resultado(self.stacked_widget)
        self.home_window = HomeWindow(self.stacked_widget)

        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.register_window)
        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.guia_window)
        self.stacked_widget.addWidget(self.pergunta1_window)
        self.stacked_widget.addWidget(self.pergunta2_window)
        self.stacked_widget.addWidget(self.pergunta3_window)
        self.stacked_widget.addWidget(self.pergunta7_window)
        self.stacked_widget.addWidget(self.pergunta8_window)
        self.stacked_widget.addWidget(self.pergunta9_window)
        self.stacked_widget.addWidget(self.pergunta10_window)
        self.stacked_widget.addWidget(self.pergunta11_window)
        self.stacked_widget.addWidget(self.pergunta12_window)
        self.stacked_widget.addWidget(self.pergunta13_window)
        self.stacked_widget.addWidget(self.pergunta14_window)
        self.stacked_widget.addWidget(self.pergunta15_window)
        self.stacked_widget.addWidget(self.pergunta16_window)
        self.stacked_widget.addWidget(self.pergunta17_window)
        self.stacked_widget.addWidget(self.pergunta18_window)
        self.stacked_widget.addWidget(self.pergunta19_window)
        self.stacked_widget.addWidget(self.pergunta20_window)
        self.stacked_widget.addWidget(self.pergunta21_window)
        self.stacked_widget.addWidget(self.pergunta22_window)
        self.stacked_widget.addWidget(self.pergunta23_window)
        self.stacked_widget.addWidget(self.pergunta24_window)
        self.stacked_widget.addWidget(self.pergunta25_window)
        self.stacked_widget.addWidget(self.pergunta26_window)
        self.stacked_widget.addWidget(self.pergunta27_window)
        self.stacked_widget.addWidget(self.resultado_window)
        self.stacked_widget.addWidget(self.home_window)

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
