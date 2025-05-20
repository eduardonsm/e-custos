from PySide6.QtWidgets import QFrame, QSlider, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap

from PySide6.QtCore import Qt
class Pergunta5Window(QWidget):

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
            v_layout = QVBoxLayout()
            pergunta = QLabel('Caso a sua empresa produza em lotes, qual seria o tamanho médio do lote para os seus principais produtos?')
            pergunta.setObjectName("pergunta")
            pergunta.setWordWrap(True)
            pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            v_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)           

            #slider container
            slider_container = QHBoxLayout()
            self.min_label = QLabel("Até 100 unidades")
            self.max_label = QLabel("Mais de 10.000 unidades")

            self.slider = QSlider(Qt.Horizontal)
            self.slider.setMinimum(0)
            self.slider.setMaximum(100)
            self.slider.setValue(50)
            self.slider.setTickPosition(QSlider.TicksBelow)
            self.slider.setTickInterval(10)
            slider_container.addWidget(self.min_label)
            slider_container.addWidget(self.slider)
            slider_container.addWidget(self.max_label)

            self.value_label = QLabel("Valor atual: 5000")
            self.slider.valueChanged.connect(self.update_label)
            self.value_label.setAlignment(Qt.AlignCenter)

            v_layout.addLayout(slider_container)

            v_layout.addWidget(self.value_label)
    
                
            #radio buttons
            radio_layout = QVBoxLayout()
            radio1 = QRadioButton("Não sei responder")
            
            radio_layout.addWidget(radio1, alignment=Qt.AlignmentFlag.AlignLeft)

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
            self.setLayout(layout)
    def switch_to_welcome(self):
        self.stacked_widget.setCurrentIndex(7)
    def avancar(self):
        self.stacked_widget.setCurrentIndex(9)
    def update_label(self, value):
        self.value_label.setText(f"Valor atual: {int(100 + (value / 100) * (10000 - 100))}")