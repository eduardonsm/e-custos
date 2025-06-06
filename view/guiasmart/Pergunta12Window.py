from PySide6.QtWidgets import QFrame,QScrollArea, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from model.Score import Score

from PySide6.QtCore import Qt
class Pergunta12Window(QWidget):

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
            v_layout = QVBoxLayout()
            pergunta = QLabel('Escolha entre os extremos para as seguintes opções:')
            pergunta.setObjectName("pergunta")
            pergunta.setStyleSheet("font-size: 25px;")
            pergunta.setTextInteractionFlags(Qt.TextBrowserInteraction)
            pergunta.setTextFormat(Qt.RichText)
            pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            v_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)

            #radio buttons
            layout1 = QHBoxLayout()
            label1 = QLabel("Especificação do projeto e produção")
            radio1 = QRadioButton("Fabricante")
            radio2 = QRadioButton("Cliente")
            layout1.addWidget(label1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout1.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout1.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            layout1.setContentsMargins(0, 0, 0, 0)
            self.radioGroupEspecificacao = QButtonGroup(self)
            self.radioGroupEspecificacao.addButton(radio1, 1)
            self.radioGroupEspecificacao.addButton(radio2, 2)
            self.radioGroupEspecificacao.setExclusive(True)
            container = QWidget()
            container.setLayout(layout1)
            v_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)
            #radio buttons2
            layout2 = QHBoxLayout()
            label1 = QLabel("Dimensão do volume produzido")
            radio1 = QRadioButton("Unidades/período")
            radio2 = QRadioButton("Unidades/pedido")
            layout2.addWidget(label1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout2.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout2.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            layout2.setContentsMargins(0, 0, 0, 0)
            self.radioGroupDimensao = QButtonGroup(self)
            self.radioGroupDimensao.addButton(radio1, 1)
            self.radioGroupDimensao.addButton(radio2, 2)
            self.radioGroupDimensao.setExclusive(True)
            container = QWidget()
            container.setLayout(layout2)
            v_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)
            #radio buttons3
            layout3 = QHBoxLayout()
            label1 = QLabel("Mercado de compradores")
            radio1 = QRadioButton("Muitos")
            radio2 = QRadioButton("Poucos")
            layout3.addWidget(label1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout3.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout3.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            layout3.setContentsMargins(0, 0, 0, 0)
            self.radioGroupMercado = QButtonGroup(self)
            self.radioGroupMercado.addButton(radio1, 1)
            self.radioGroupMercado.addButton(radio2, 2)
            self.radioGroupMercado.setExclusive(True)
            container = QWidget()
            container.setLayout(layout3)
            v_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)
            #radio buttons4
            layout4 = QHBoxLayout()
            label1 = QLabel("Atendimento ao mercado")
            radio1 = QRadioButton("Genérico")
            radio2 = QRadioButton("Específico")
            layout4.addWidget(label1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout4.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout4.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            layout4.setContentsMargins(0, 0, 0, 0)
            self.radioGroupAtendimento = QButtonGroup(self)
            self.radioGroupAtendimento.addButton(radio1, 1)
            self.radioGroupAtendimento.addButton(radio2, 2)
            self.radioGroupAtendimento.setExclusive(True)
            container = QWidget()
            container.setLayout(layout4)
            v_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)
            #radio buttons5
            layout5 = QHBoxLayout()
            label1 = QLabel("Estoque de matéria-prima")
            radio1 = QRadioButton("Indispensável")
            radio2 = QRadioButton("Temporário")
            layout5.addWidget(label1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout5.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout5.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            layout5.setContentsMargins(0, 0, 0, 0)
            self.radioGroupMateriaPrima = QButtonGroup(self)
            self.radioGroupMateriaPrima.addButton(radio1, 1)
            self.radioGroupMateriaPrima.addButton(radio2, 2)
            self.radioGroupMateriaPrima.setExclusive(True)
            container = QWidget()
            container.setLayout(layout5)
            v_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)
            #radio buttons6
            layout6 = QHBoxLayout()
            label1 = QLabel("Estoque de produtos acabados")
            radio1 = QRadioButton("Necessário")
            radio2 = QRadioButton("Indesejável")
            layout6.addWidget(label1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout6.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            layout6.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            layout6.setContentsMargins(0, 0, 0, 0)
            self.radioGroupProdutosAcabados = QButtonGroup(self)
            self.radioGroupProdutosAcabados.addButton(radio1, 1)
            self.radioGroupProdutosAcabados.addButton(radio2, 2)
            self.radioGroupProdutosAcabados.setExclusive(True)
            container = QWidget()
            container.setLayout(layout6)
            v_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)

            self.naoSeiResponder = QRadioButton("Nao sei responder")
            self.naoSeiResponder.setMaximumWidth(300)
            v_layout.addWidget(self.naoSeiResponder, alignment=Qt.AlignmentFlag.AlignCenter)

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
        self.responder(index-1)
        self.stacked_widget.setCurrentIndex(index + 1)
    def responder(self, index):

        if self.naoSeiResponder.isChecked():
            respostaEspecificacao = None
            respostaDimensao = None
            respostaMercado = None
            respostaAtendimento = None
            respostaMateriaPrima = None
            respostaProdutosAcabados = None
        else:
            respostaEspecificacao = self.radioGroupEspecificacao.id(self.radioGroupEspecificacao.checkedButton())+58
            respostaDimensao = self.radioGroupDimensao.id(self.radioGroupDimensao.checkedButton())+60
            respostaMercado = self.radioGroupMercado.id(self.radioGroupMercado.checkedButton())+62
            respostaAtendimento = self.radioGroupAtendimento.id(self.radioGroupAtendimento.checkedButton())+64
            respostaMateriaPrima = self.radioGroupMateriaPrima.id(self.radioGroupMateriaPrima.checkedButton())+66
            respostaProdutosAcabados = self.radioGroupProdutosAcabados.id(self.radioGroupProdutosAcabados.checkedButton())+68

        score = Score()
        score.adicionarLinha(index, respostaEspecificacao)
        score.adicionarLinha(index+1, respostaDimensao)
        score.adicionarLinha(index+2, respostaMercado)
        score.adicionarLinha(index+3, respostaAtendimento)
        score.adicionarLinha(index+4, respostaMateriaPrima)
        score.adicionarLinha(index+5, respostaProdutosAcabados)
        print("Respostas até agora:", score.getRespostas())