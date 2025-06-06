from PySide6.QtWidgets import QFrame,QScrollArea, QSlider, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from model.Score import Score
from model.utils import transformar_para_escala_1_3

from PySide6.QtCore import Qt
class Pergunta8Window(QWidget):

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
            label = QLabel("Flexibilidade dos recursos")
            self.flexibilidadeSlider = QSlider(Qt.Horizontal)
            self.flexibilidadeSlider.setRange(0, 100)
            self.flexibilidadeSlider.setValue(50)
            self.flexibilidadeSlider.setTickPosition(QSlider.TicksBelow)
            self.flexibilidadeSlider.setTickInterval(10)
            self.flexibilidadeSlider.setFixedWidth(150)
            v_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            v_layout.addWidget(self.flexibilidadeSlider, alignment=Qt.AlignmentFlag.AlignCenter)

            #slider container
            slider_container = QHBoxLayout()
            self.min_label = QLabel("Lead-time de atravessamento")
            self.max_label = QLabel("Produtividade")

            self.leadSlider = QSlider(Qt.Vertical)
            self.leadSlider.setRange(0, 100)
            self.leadSlider.setValue(50)
            self.leadSlider.setTickPosition(QSlider.TicksBelow)
            self.leadSlider.setTickInterval(10)
            self.leadSlider.setFixedHeight(150)

            slider_container.setContentsMargins(0,0,0,0)
            slider_container.addWidget(self.min_label)

            self.produtividadeSlider = QSlider(Qt.Vertical)
            self.produtividadeSlider.setRange(0, 100)
            self.produtividadeSlider.setValue(50)
            self.produtividadeSlider.setTickPosition(QSlider.TicksBelow)
            self.produtividadeSlider.setTickInterval(10)
            self.produtividadeSlider.setFixedHeight(150)

            slider_container.addWidget(self.leadSlider)
            
            icon = QLabel()
            icon.setFixedSize(250, 160)  # Tamanho fixo
            icon.setScaledContents(True)
            pixmap = QPixmap("./images/dimensoes.png")
            icon.setPixmap(pixmap)
            icon.setAlignment(Qt.AlignCenter)
            slider_container.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)

            slider_container.addWidget(self.produtividadeSlider)
            slider_container.addWidget(self.max_label)

            self.value_label = QLabel("Padronização do produto")
            self.value_label.setAlignment(Qt.AlignCenter)

            v_layout.addLayout(slider_container)
            self.padronizacaoSlider = QSlider(Qt.Horizontal)
            self.padronizacaoSlider.setRange(0, 100)
            self.padronizacaoSlider.setValue(50)
            self.padronizacaoSlider.setTickPosition(QSlider.TicksBelow)
            self.padronizacaoSlider.setTickInterval(10)
            self.padronizacaoSlider.setFixedWidth(150)

            v_layout.addWidget(self.padronizacaoSlider, alignment=Qt.AlignmentFlag.AlignCenter)
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
        self.responder(index-4)
        self.stacked_widget.setCurrentIndex(index + 1)

    def responder(self, index):
        score = Score()

        if self.radio1.isChecked():
            respostaFlexibilidade = None
            respostaLead = None
            respostaProdutividade = None
            respostaPadronizacao = None
        else:
            flexibilidade_original = self.flexibilidadeSlider.value()
            lead_original = self.leadSlider.value()
            produtividade_original = self.produtividadeSlider.value()
            padronizacao_original = self.padronizacaoSlider.value()

            respostaFlexibilidade = 23+transformar_para_escala_1_3(flexibilidade_original)
            respostaLead = 26+transformar_para_escala_1_3(lead_original)
            respostaProdutividade = 29+transformar_para_escala_1_3(produtividade_original)
            respostaPadronizacao = 32+transformar_para_escala_1_3(padronizacao_original)

        score.adicionarLinha(index, respostaFlexibilidade)
        score.adicionarLinha(index + 1, respostaLead)
        score.adicionarLinha(index + 2, respostaProdutividade)
        score.adicionarLinha(index + 3, respostaPadronizacao)
        print("Respostas até agora:", score.getRespostas())
