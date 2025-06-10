from PySide6.QtWidgets import QFrame,QScrollArea, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from components.CustomRadioButton import CustomRadioButton
from model.Score import Score

from PySide6.QtCore import Qt
class Pergunta10Window(QWidget):

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
            pergunta = QLabel('Qual desses arranjos físicos o seu sistema produtivo mais se aproxima? Um layout híbrido pode ser utilizado')
            pergunta.setObjectName("pergunta")
            pergunta.setWordWrap(True)
            pergunta.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
            pergunta.setMinimumWidth(850)
            pergunta.setMinimumHeight(100)
            pergunta.setStyleSheet("font-size: 30px;")  # Definindo o tamanho da fonte
            v_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)
            
            
            #radio buttons
            group = QButtonGroup(self)
            radio1 = CustomRadioButton("Fluxo em linha","./images/LINHA.jpeg",group,1)
            radio2 = CustomRadioButton("Fluxo em célula","./images/LINHA.jpeg",group,2)
            radio3 = CustomRadioButton("Fluxo por processos","",group,3)

            radio4 = CustomRadioButton("Fluxo posicional","./images/LINHA.jpeg",group,4)
            radio5 = CustomRadioButton("Arranjo Híbrido","./images/LINHA.jpeg",group,5)
            radio6 = CustomRadioButton("Não sei responder","",group,6)
            group.setExclusive(True)
            self.radio_group = group

            h_layout = QHBoxLayout()
            v_layout1 = QVBoxLayout()
            v_layout1.addWidget(radio1)
            v_layout1.addWidget(radio2)
            v_layout1.addWidget(radio3)
            v_layout2 = QVBoxLayout()
            v_layout2.addWidget(radio4)
            v_layout2.addWidget(radio5)
            v_layout2.addWidget(radio6)
            h_layout.addLayout(v_layout1)
            h_layout.addLayout(v_layout2)
            h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            pergunta_container = QWidget()
            pergunta_container.setLayout(v_layout)
            layout.addWidget(pergunta_container)
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

            layout.setContentsMargins(20, 5, 20, 20)
            layout.setSpacing(10)
            # self.setLayout(layout)
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            # Conteúdo real da tela
            content_widget = QWidget()
            content_widget.setLayout(layout)

            scroll_area.setWidget(content_widget)

            # Layout final da tela com rolagem
            final_layout = QVBoxLayout()
            final_layout.addWidget(scroll_area)
            self.setLayout(final_layout)

    def switch_to_welcome(self):
        index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(index -1)
    def avancar(self):
        index = self.stacked_widget.currentIndex()
        self.responder(index+4)
        self.stacked_widget.setCurrentIndex(index + 1)
    def responder(self, index):

        checked_button = self.radio_group.checkedButton()

        for btn in self.findChildren(CustomRadioButton):
            if btn.isChecked():
                texto = btn.text()
        if texto == "Não sei responder":
            resposta = None
        else:
            resposta = self.radio_group.id(checked_button)+47

        score = Score()
        score.adicionarLinha(index, resposta)
        print("Respostas até agora:", score.getRespostas())
    