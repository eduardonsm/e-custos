from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from model.Score import Score

from PySide6.QtCore import Qt
class Pergunta11Window(QWidget):

    def __init__(self, stacked_widget):
            super().__init__()
            self.stacked_widget = stacked_widget
            layout = QVBoxLayout()

            #header
            h_layout = QHBoxLayout()
            titulo = QLabel("AMBIENTE PRODUTIVO")
            titulo.setObjectName("titulo")

            h_layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignLeft)
            icon = QLabel()
            pixmap = QPixmap("./images/ecustos-logo.png").scaled(170, 170, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
            pergunta = QLabel('Qual seria uma eficiência média diária da capacidade para o seu ambiente produtivo? \nConsidere, por exemplo, que seu ambiente tenha capacidade de produzir 100 peças dia e entrega 60. A capacidade seria [60/100]*100 = 60%')
            pergunta.setObjectName("pergunta")
            pergunta.setWordWrap(True)
            pergunta.setStyleSheet("font-size: 25px;")
            pergunta.setTextInteractionFlags(Qt.TextBrowserInteraction)
            pergunta.setTextFormat(Qt.RichText)
            pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            h_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignLeft)           

            #radio buttons
            radio_layout = QVBoxLayout()
            radio1 = QRadioButton("Até 9%")
            radio2 = QRadioButton("Entre 10 e 20%")
            radio3 = QRadioButton("Entre 21 e 40%")
            radio4 = QRadioButton("Entre 41 e 60%")
            radio5 = QRadioButton("Entre 61 e 80%")
            radio6 = QRadioButton("Entre 81 e 100%")
            radio7 = QRadioButton("Não sei responder")

            style = "QRadioButton { min-height: 20px; }"
            for radio in [radio1, radio2, radio3, radio4, radio5, radio6, radio7]:
                radio.setStyleSheet(style)

            radio_layout.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio3, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio4, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio5, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio6, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio7, alignment=Qt.AlignmentFlag.AlignLeft)

            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.setSpacing(16)
            radio_group = QButtonGroup(self)
            radio_group.addButton(radio1, 1)
            radio_group.addButton(radio2, 2)
            radio_group.addButton(radio3, 3)
            radio_group.addButton(radio4, 4)
            radio_group.addButton(radio5, 5)
            radio_group.addButton(radio6, 6)
            radio_group.addButton(radio7, 7)
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
        self.responder(index+4)
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
            resposta = self.radio_group.id(checked_button)+52

        score = Score()
        score.adicionarLinha(index, resposta)
        print("Respostas até agora:", score.getRespostas())