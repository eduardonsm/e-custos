from PySide6.QtWidgets import QFrame,QScrollArea, QSlider, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QButtonGroup, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QCursor, QPixmap

from PySide6.QtCore import Qt
class Pergunta7Window(QWidget):

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
            v_layout.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)

            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(50)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(10)
            slider.setFixedWidth(150)
            v_layout.addWidget(slider, alignment=Qt.AlignmentFlag.AlignCenter)

            #slider container
            slider_container = QHBoxLayout()
            self.min_label = QLabel("Volatilidade na demanda")
            self.max_label = QLabel("Variedade do mix")

            self.slider1 = QSlider(Qt.Vertical)
            self.slider1.setRange(0, 100)
            self.slider1.setValue(50)
            self.slider1.setTickPosition(QSlider.TicksBelow)
            self.slider1.setTickInterval(10)
            self.slider1.setFixedHeight(150)

            slider_container.setContentsMargins(0,0,0,0)
            slider_container.addWidget(self.min_label)

            self.slider2 = QSlider(Qt.Vertical)
            self.slider2.setRange(0, 100)
            self.slider2.setValue(50)
            self.slider2.setTickPosition(QSlider.TicksBelow)
            self.slider2.setTickInterval(10)
            self.slider2.setFixedHeight(150)
            
            slider_container.addWidget(self.slider1)
            
            icon = QLabel()
            icon.setFixedSize(250, 160)  # Tamanho fixo
            icon.setScaledContents(True)
            pixmap = QPixmap("./images/dimensoes.png")
            icon.setPixmap(pixmap)
            icon.setAlignment(Qt.AlignCenter)
            slider_container.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)

            slider_container.addWidget(self.slider2)
            slider_container.addWidget(self.max_label)

            self.value_label = QLabel("Valor atual: 50%")
            self.slider1.valueChanged.connect(self.update_label)
            self.value_label.setAlignment(Qt.AlignCenter)

            v_layout.addLayout(slider_container)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(50)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(10)
            slider.setFixedWidth(150)

            v_layout.addWidget(slider, alignment=Qt.AlignmentFlag.AlignCenter)
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
        self.stacked_widget.setCurrentIndex(9)
    def avancar(self):
        self.stacked_widget.setCurrentIndex(11)
    def update_label(self, value):
        self.value_label.setText(f"Valor atual: {value}%")