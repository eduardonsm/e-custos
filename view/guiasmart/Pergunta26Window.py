from PySide6.QtWidgets import QFrame, QScrollArea,QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from model.Score import Score
from PySide6.QtCore import Qt
class Pergunta26Window(QWidget):

    def __init__(self, stacked_widget):
            super().__init__()
            self.stacked_widget = stacked_widget
            layout = QVBoxLayout()

            #header
            h_layout = QHBoxLayout()
            titulo = QLabel("CUSTOS E INFORMAÇOES")
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
            pergunta = QLabel('Para fins de sua análise, qual seria o objetivo da formação de custos na sua empresa?')
            pergunta.setObjectName("pergunta")
            pergunta.setWordWrap(True)
            pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            h_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignLeft)           

            #radio buttons
            radio_layout = QVBoxLayout()
            radio1 = QRadioButton("Avaliar estoques")
            radio2 = QRadioButton("Controlar os custos com base em um padrão")
            radio3 = QRadioButton("Decisões a partir de detalhamento nos custos")
            radio4 = QRadioButton("Eliminar custos fixos desnecessários")
            radio5 = QRadioButton("Avaliar atividades que não agregam valor")
            radio6 = QRadioButton("Analisar o impacto do custo de transformação")
            radio7 = QRadioButton("Utilizar bases mais simples de custeio")
            radio8 = QRadioButton("Usar bases mais adequadas, porém complexas")
            radio9 = QRadioButton("Uniformizar as medidas de produção")
            radio10 = QRadioButton("Não sei responder")
            

            radio_layout.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio3, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio4, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio5, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio6, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio7, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio8, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio9, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio10, alignment=Qt.AlignmentFlag.AlignLeft)

            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.setSpacing(20)
            radio_group = QButtonGroup(self)
            radio_group.addButton(radio1, 1)
            radio_group.addButton(radio2, 2)
            radio_group.addButton(radio3, 3)
            radio_group.addButton(radio4, 4)
            radio_group.addButton(radio5, 5)
            radio_group.addButton(radio6, 6)
            radio_group.addButton(radio7, 7)
            radio_group.addButton(radio8, 8)
            radio_group.addButton(radio9, 9)
            radio_group.addButton(radio10, 10)
            radio_group.setExclusive(True)
            self.radio_group = radio_group

            style = "QRadioButton { min-height: 20px; }"
            for radio in [radio1, radio2, radio3, radio4,radio5, radio6, radio7, radio8,radio9,radio10]:
                radio.setStyleSheet(style)

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

        if checked_button is None:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione uma opção antes de avançar.")
            return

        texto = checked_button.text()
        if texto == "Não sei responder":
            resposta = None
        else:
            resposta = self.radio_group.id(checked_button)+135

        score = Score()
        score.adicionarLinha(index, resposta)
        print("Respostas até agora:", score.getRespostas())