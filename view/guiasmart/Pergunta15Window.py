from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from model.Score import Score

from PySide6.QtCore import Qt
class Pergunta15Window(QWidget):

    def __init__(self, stacked_widget):
            super().__init__()
            self.stacked_widget = stacked_widget
            layout = QVBoxLayout()

            #header
            h_layout = QHBoxLayout()
            titulo = QLabel("FATORES DE PRODUÇAO")
            titulo.setObjectName("titulo")

            h_layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignLeft)
            icon = QLabel()
            pixmap = QPixmap("./images/ecustos-logo.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon.setPixmap(pixmap)
            icon.setAlignment(Qt.AlignCenter)
            h_layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignRight)

            container = QWidget()
            container.setLayout(h_layout)
            layout.addWidget(container)
            # separando
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 3px;")
            layout.addWidget(line)

            # main
            h_layout = QHBoxLayout()
            pergunta = QLabel('Sobre a flexibilidade de máquinas, equipamentos, ferramentas e pessoas para realizar diversas funções, como você avalia o nível de adaptação desses ativos para executar diferentes tipos de processos?')
            pergunta.setObjectName("pergunta")
            pergunta.setWordWrap(True)
            pergunta.setOpenExternalLinks(False)  
            pergunta.setTextInteractionFlags(Qt.TextBrowserInteraction)
            pergunta.setTextFormat(Qt.RichText)
            pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            h_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignLeft)           

            #radio buttons
            radio_layout = QVBoxLayout()
            radio1 = QRadioButton("Baixíssima flexibilidade")
            radio2 = QRadioButton("Baixa flexibilidade")
            radio3 = QRadioButton("Moderada flexibilidade")
            radio4 = QRadioButton("Alta flexibilidade")
            radio5 = QRadioButton("Altissima flexibilidade")
            radio6 = QRadioButton("Não sei responder")
            

            radio_layout.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio3, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio4, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio5, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio6, alignment=Qt.AlignmentFlag.AlignLeft)

            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.setSpacing(20)
            radio_group = QButtonGroup(self)
            radio_group.addButton(radio1, 1)
            radio_group.addButton(radio2, 2)
            radio_group.addButton(radio3, 3)
            radio_group.addButton(radio4, 4)
            radio_group.addButton(radio5, 5)
            radio_group.addButton(radio6, 6)
            radio_group.setExclusive(True)
            self.radio_group = radio_group

            container = QWidget()
            container.setLayout(radio_layout)
            h_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)
            main_container = QWidget()
            main_container.setLayout(h_layout)
            layout.addWidget(main_container)

            # separando
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 3px;")
            layout.addWidget(line)

            
            container = QHBoxLayout()
            #botao de voltar
            voltar = QPushButton("VOLTAR PARA A TELA ANTERIOR!")
            voltar.setCursor(QCursor(Qt.PointingHandCursor))
            voltar.clicked.connect(self.switch_to_welcome)
            container.addWidget(voltar, alignment=Qt.AlignmentFlag.AlignLeft)

            #botao de avancar
            avancar = QPushButton("PODE AVANÇAR!")
            avancar.setCursor(QCursor(Qt.PointingHandCursor))
            avancar.clicked.connect(self.avancar)
            container.addWidget(avancar, alignment=Qt.AlignmentFlag.AlignRight)

            container.setContentsMargins(50, 0, 50, 0)
            layout.addLayout(container)

            #adicionando o layout ao widget
            layout.setContentsMargins(20, 5, 20, 20)
            layout.setSpacing(10)
            self.setLayout(layout)
    def switch_to_welcome(self):
        index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(index -1)
    def avancar(self):
        index = self.stacked_widget.currentIndex()
        self.responder(index+9)
        self.stacked_widget.setCurrentIndex(index + 1)
    def responder(self, index):
        checked_button = self.radio_group.checkedButton()

        if checked_button is None:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione uma opção antes de avançar.")
            return

        texto = checked_button.text()
        if texto == "Não sei responder":
            resposta = None
        else:
            resposta = self.radio_group.id(checked_button)+78

        score = Score()
        score.adicionarLinha(index, resposta)
        print("Respostas até agora:", score.getRespostas())