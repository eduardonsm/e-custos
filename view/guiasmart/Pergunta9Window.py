from PySide6.QtWidgets import QFrame,QScrollArea, QSlider, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from model.Score import Score
from model.utils import transformar_para_escala_1_3

from PySide6.QtCore import Qt
class Pergunta9Window(QWidget):

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
            pergunta = QLabel('Posicione o slide em cada dimensão para representar o quão sua empresa se enquadra.')
            pergunta.setObjectName("pergunta")
            pergunta.setWordWrap(True)
            pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            pergunta.setStyleSheet("font-size: 30px;")  # Definindo o tamanho da fonte
            v_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)
            label = QLabel("Automação do processo")
            self.automacaoSlider = QSlider(Qt.Horizontal)
            self.automacaoSlider.setRange(0, 100)
            self.automacaoSlider.setValue(50)
            self.automacaoSlider.setTickPosition(QSlider.TicksBelow)
            self.automacaoSlider.setTickInterval(10)
            self.automacaoSlider.setFixedWidth(150)
            v_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            v_layout.addWidget(self.automacaoSlider, alignment=Qt.AlignmentFlag.AlignCenter)

            #slider container
            slider_container = QHBoxLayout()
            self.min_label = QLabel("Rendimento da capacidade")
            self.max_label = QLabel("Força de trabalho")

            self.rendimentoSlider = QSlider(Qt.Vertical)
            self.rendimentoSlider.setRange(0, 100)
            self.rendimentoSlider.setValue(50)
            self.rendimentoSlider.setTickPosition(QSlider.TicksBelow)
            self.rendimentoSlider.setTickInterval(10)
            self.rendimentoSlider.setFixedHeight(150)

            slider_container.setContentsMargins(0,0,0,0)
            slider_container.addWidget(self.min_label)

            self.forcaTrabalhoSlider = QSlider(Qt.Vertical)
            self.forcaTrabalhoSlider.setRange(0, 100)
            self.forcaTrabalhoSlider.setValue(50)
            self.forcaTrabalhoSlider.setTickPosition(QSlider.TicksBelow)
            self.forcaTrabalhoSlider.setTickInterval(10)
            self.forcaTrabalhoSlider.setFixedHeight(150)

            slider_container.addWidget(self.rendimentoSlider)

            icon = QLabel()
            icon.setFixedSize(250, 160)  # Tamanho fixo
            icon.setScaledContents(True)
            pixmap = QPixmap("./images/dimensoes.png")
            icon.setPixmap(pixmap)
            icon.setAlignment(Qt.AlignCenter)
            slider_container.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)

            slider_container.addWidget(self.forcaTrabalhoSlider)
            slider_container.addWidget(self.max_label)

            self.value_label = QLabel("Agregação de valor")
            self.value_label.setAlignment(Qt.AlignCenter)

            v_layout.addLayout(slider_container)
            self.agregacaoSlider = QSlider(Qt.Horizontal)
            self.agregacaoSlider.setRange(0, 100)
            self.agregacaoSlider.setValue(50)
            self.agregacaoSlider.setTickPosition(QSlider.TicksBelow)
            self.agregacaoSlider.setTickInterval(10)
            self.agregacaoSlider.setFixedWidth(150)

            v_layout.addWidget(self.agregacaoSlider, alignment=Qt.AlignmentFlag.AlignCenter)
            v_layout.addWidget(self.value_label)

            #radio buttons
            radio_layout = QVBoxLayout()
            self.radio1 = QRadioButton("Não sei responder")

            radio_layout.addWidget(self.radio1, alignment=Qt.AlignmentFlag.AlignLeft)

            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.setSpacing(10)

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
        self.responder(index+1)
        self.stacked_widget.setCurrentIndex(index + 1)

    def responder(self, index):
        score = Score()

        if self.radio1.isChecked():
            respostaAutomacao = None
            respostaRendimento = None
            respostaForcaTrabalho = None
            respostaAgregacao = None
        else:
            automacao_original = self.automacaoSlider.value()
            rendimento_original = self.rendimentoSlider.value()
            forca_trabalho_original = self.forcaTrabalhoSlider.value()
            agregacao_original = self.agregacaoSlider.value()

            respostaAutomacao = 35+transformar_para_escala_1_3(automacao_original)
            respostaRendimento = 38+transformar_para_escala_1_3(rendimento_original)
            respostaForcaTrabalho = 41+transformar_para_escala_1_3(forca_trabalho_original)
            respostaAgregacao = 44+transformar_para_escala_1_3(agregacao_original)

        score.adicionarLinha(index, respostaAutomacao)
        score.adicionarLinha(index + 1, respostaRendimento)
        score.adicionarLinha(index + 2, respostaForcaTrabalho)
        score.adicionarLinha(index + 3, respostaAgregacao)
        print("Respostas até agora:", score.getRespostas())
    