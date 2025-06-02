from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtCore import Qt
from model.Score import Score
class Pergunta3Window(QWidget):

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
            pixmap = QPixmap("./images/ecustos-logo.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
            v_layout = QVBoxLayout()
            pergunta = QLabel('Qual desses tipos de tecnologias de produção o seu ambiente mais se enquadra?')
            pergunta.setObjectName("pergunta")
            pergunta.setWordWrap(True)
            pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            v_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)           

            #radio buttons
            radio_layout = QVBoxLayout()
            radio_group = QButtonGroup(self)
            radio1 = QRadioButton("Produção tradicional: métodos manuais e/ou parcialmente mecanizados, com alta importância do trabalho humano")
            radio2 = QRadioButton("Produção automatizada: maior uso de máquinas e equipamentos automatizados, produção rápida, eficiente, com inserção de controles para automação")
            radio3 = QRadioButton("Produção avançada: uso de tecnologias avançadas, tais como manufatura aditiva, sistemas inteligentes e robóticos, internet das coisas, etc.")
            radio4 = QRadioButton("Produção sustentável: foco em processo com baixo impacto ambiental, eficiente uso dos recursos, baixa geração de resíduos, economia circular, etc")
            radio5 = QRadioButton("Produção flexível: as máquinas e equipamentos são configurados para alta adaptação à demanda. ")
            radio6 = QRadioButton("Não sei responder")
            

            radio_layout.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio3, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio4, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio5, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio6, alignment=Qt.AlignmentFlag.AlignLeft)

            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.setSpacing(10)
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
            v_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)
            main_container = QWidget()
            main_container.setLayout(v_layout)
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
        self.stacked_widget.setCurrentIndex(5)
    def avancar(self):
        index = self.stacked_widget.currentIndex()
        self.responder(index-4)
        self.stacked_widget.setCurrentIndex(index + 1)
    def responder(self, index):

        checked_button = self.radio_group.checkedButton()
        if not checked_button:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione uma opção antes de avançar.")
            return

        texto = checked_button.text()
        if texto == "Não sei responder":
            resposta = None
        else:
            resposta = self.radio_group.id(checked_button)+9

        score = Score()
        score.adicionarLinha(index, resposta)
        print("Respostas até agora:", score.getRespostas())