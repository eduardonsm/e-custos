from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtCore import Qt
from model.Score import Score
class Pergunta18Window(QWidget):

    def __init__(self, stacked_widget):
            super().__init__()
            self.stacked_widget = stacked_widget
            layout = QVBoxLayout()

            #header
            h_layout = QHBoxLayout()
            titulo = QLabel("LOGISTICA")
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
            pergunta = QLabel('Em qual tipo de estoque recai o seu maior interesse de análise?')
            pergunta.setObjectName("pergunta")
            pergunta.setWordWrap(True)
            pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            pergunta.setMinimumWidth(850)
            pergunta.setMinimumHeight(100)
            pergunta.setStyleSheet("font-size: 30px;")  # Definindo o tamanho da fonte
            v_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)           

            #radio buttons
            radio_layout = QVBoxLayout()
            radio_group = QButtonGroup(self)
            radio1 = QRadioButton("Estoque de matéria-prima, componentes, insumos, entre outros materiais diretos (antes do uso)")
            radio2 = QRadioButton("Estoque em processo de materiais, matéria-prima, componentes, insumos, etc. (no uso)")
            radio3 = QRadioButton("Estoque de produto acabado, semiacabado, grupos de montagens (finalizado)")
            radio4 = QRadioButton("Não sei responder")
            

            radio_layout.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio2, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio3, alignment=Qt.AlignmentFlag.AlignLeft)
            radio_layout.addWidget(radio4, alignment=Qt.AlignmentFlag.AlignLeft)

            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.setSpacing(10)
            radio_group.addButton(radio1, 1)
            radio_group.addButton(radio2, 2)
            radio_group.addButton(radio3, 3)
            radio_group.addButton(radio4, 4)
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
            resposta = self.radio_group.id(checked_button)+94

        score = Score()
        score.adicionarLinha(index, resposta)
        print("Respostas até agora:", score.getRespostas())