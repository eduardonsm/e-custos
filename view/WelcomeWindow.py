from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QIcon, QPixmap
from components.CustomRadioButton import CustomRadioButton
from model.Session import Session
import sqlite3

from PySide6.QtCore import Qt
class Welcome(QWidget):
    
    # Tela de boas-vindas.


    def __init__(self, stacked_widget):
            super().__init__()
            self.stacked_widget = stacked_widget
            layout = QVBoxLayout()


            #boas vindas
            h_layout = QHBoxLayout()
            bemvindo = QLabel("SEJA BEM VINDO(A) AO E-CUSTO$ !")
            bemvindo.setObjectName("titulo")
            h_layout.addWidget(bemvindo, alignment=Qt.AlignmentFlag.AlignLeft)
            icon = QLabel()
            pixmap = QPixmap("./images/ecustos-logo.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon.setPixmap(pixmap)
            icon.setAlignment(Qt.AlignCenter)

            h_layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignRight)

            container = QWidget()
            container.setLayout(h_layout)
            layout.addWidget(container)


            titulo = QLabel('Se você já sabe qual princípio e qual método utilizar, favor selecioná-los. Se não, clique no <a href="#" style="color: #8faadc;font-weight: 800;">Guia $mart!</a>')
            titulo.setWordWrap(True)
            titulo.setAlignment(Qt.AlignCenter)
            titulo.setOpenExternalLinks(False)  
            titulo.setTextInteractionFlags(Qt.TextBrowserInteraction)
            titulo.setTextFormat(Qt.RichText)
            titulo.linkActivated.connect(lambda: self.switch_to_guia())  # Conecta o clique do link a uma função
            titulo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            layout.addWidget(titulo)

            

            # separando
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 3px;")
            layout.addWidget(line)

            #principio
            principio = QLabel("Princípio:")
            # Radio buttons
            radio1 = QRadioButton("Integral")
            icon = QIcon("./images/integral.png")
            radio1.setIcon(icon)
            radio1.setIconSize(radio1.sizeHint()) 
            radio2 = QRadioButton("Variável")
            icon = QIcon("./images/variavel.png")
            radio2.setIcon(icon)
            radio2.setIconSize(radio2.sizeHint()) 
            radio3 = QRadioButton("Ideal")
            icon = QIcon("./images/ideal.png")
            radio3.setIcon(icon)
            radio3.setIconSize(radio3.sizeHint()) 

            # Agrupar os botões para garantir seleção única
            self.principio_group = QButtonGroup()
            self.principio_group.addButton(radio1)
            self.principio_group.addButton(radio2)
            self.principio_group.addButton(radio3)

            h_layout = QHBoxLayout()
            h_layout.addWidget(principio)
            h_layout.addWidget(radio1)
            h_layout.addWidget(radio2)
            h_layout.addWidget(radio3)

            container = QWidget()
            container.setLayout(h_layout)
            layout.addWidget(container)

            # separando
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 3px;")
            layout.addWidget(line)

            # metodo
            metodo = QLabel("Método:")
            self.metodo_group = QButtonGroup(self)
            radio1 = CustomRadioButton("Simples","./images/simples.png",self.metodo_group,1)
            radio2 = CustomRadioButton("RKW","./images/rkw.png",self.metodo_group,2)
            radio3 = CustomRadioButton("UEP","./images/uep.png",self.metodo_group,3)
            radio4 = CustomRadioButton("ABC","./images/abc.png",self.metodo_group,4)
            radio5 = CustomRadioButton("TDABC","./images/tdabc.png",self.metodo_group,5)
            radio6 = CustomRadioButton("Gecon","./images/gecon.png",self.metodo_group,6)
            self.metodo_group.setExclusive(True)

            h_layout = QHBoxLayout()
            h_layout.addWidget(metodo)
            h_layout.addWidget(radio1)
            h_layout.addWidget(radio2)
            h_layout.addWidget(radio3)
            h_layout.addWidget(radio4)
            h_layout.addWidget(radio5)
            h_layout.addWidget(radio6)

            container = QWidget()
            container.setLayout(h_layout)
            layout.addWidget(container)

            #botao de selecionar
            selecionar = QPushButton("SELECIONAR")
            selecionar.setStyleSheet("background-color: #2196F3; color: white;")
            selecionar.clicked.connect(lambda: self.salvar_metodo_principio())

            layout.addWidget(selecionar, alignment=Qt.AlignmentFlag.AlignRight)

            #adicionando o layout ao widget
            layout.setContentsMargins(20, 20, 20, 20)  # Margens internas
            layout.setSpacing(10)
            self.setLayout(layout)
    def switch_to_guia(self):
        # Função para mudar para a tela do guia
        self.stacked_widget.setCurrentIndex(3)

    def salvar_metodo_principio(self):
        principio = self.principio_group.checkedButton().text() if self.principio_group.checkedButton() else None
        metodo = None
        for btn in self.findChildren(CustomRadioButton):
            if btn.isChecked():
                metodo = btn.text()
                break

        session = Session()
        self.update_principio_metodo(session.user_id, metodo, principio)
        
        home_screen = self.stacked_widget.widget(29)
        home_screen.update_user_info()
        self.stacked_widget.setCurrentIndex(29)
        self.stacked_widget.setCurrentIndex(29)

    def update_principio_metodo(self, user_id, metodo, principio):
        conn = sqlite3.connect("model/LoginSystem.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET metodo = ?, principio = ?
            WHERE id = ?
        """, (metodo, principio, user_id))
        conn.commit()
        conn.close()