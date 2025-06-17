from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton, QSizePolicy
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt
from model.Score import Score

class Resultado(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 5, 20, 20)
        layout.setSpacing(15)

        # Header
        h_layout_header = QHBoxLayout()
        titulo = QLabel("MÉTODO E PRINCÍPIO DE CUSTEIO")
        titulo.setObjectName("titulo")
        h_layout_header.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignLeft)

        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        icon.setAlignment(Qt.AlignCenter)
        h_layout_header.addWidget(icon, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(h_layout_header)

        # Separador
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        line1.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 2px;")
        layout.addWidget(line1)

        # Resultados
        main_container = QVBoxLayout()
        main_container.setSpacing(10)
        main_container.setContentsMargins(20, 10, 20, 20)
        
        pergunta = QLabel('Com base nas suas respostas, a recomendação é:')
        pergunta.setObjectName("pergunta")
        pergunta.setWordWrap(True)
        pergunta.setMinimumHeight(100)
        pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        pergunta.setStyleSheet("font: bold 32px 'Inter'; color: #0f0b0b; padding: 15px;")
        main_container.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)

        self.metodo_label = QLabel("Método: -")
        self.metodo_label.setObjectName("resultado_metodo")
        self.metodo_label.setStyleSheet("font: bold 32px 'Inter'; color: #15803d; padding: 5px;")
        main_container.addWidget(self.metodo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.principio_label = QLabel("Princípio: -")
        self.principio_label.setObjectName("resultado_principio")
        self.principio_label.setStyleSheet("font: bold 32px 'Inter'; color: #1d4ed8; padding: 5px;")
        main_container.addWidget(self.principio_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(main_container)
        layout.addStretch()

        # Separador
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        line2.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 2px;")
        layout.addWidget(line2)

        # Botões
        botoes_layout = QHBoxLayout()
        botoes_layout.setContentsMargins(50, 10, 50, 0)

        voltar = QPushButton("◄ VOLTAR")
        voltar.setCursor(QCursor(Qt.PointingHandCursor))
        voltar.clicked.connect(self.switch_to_previous)
        botoes_layout.addWidget(voltar, alignment=Qt.AlignmentFlag.AlignLeft)

        avancar = QPushButton("SAIR ►")
        avancar.setCursor(QCursor(Qt.PointingHandCursor))
        avancar.clicked.connect(self.avancar)
        botoes_layout.addWidget(avancar, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(botoes_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.carregar_e_exibir_resultados()

    def carregar_e_exibir_resultados(self):
        score = Score()
        resultado = score.SelecionarMetodoPrincipio()
        if resultado and len(resultado) >= 2:
            self.metodo_label.setText(f"Método: {resultado[0]}")
            self.principio_label.setText(f"Princípio: {resultado[1]}")
        else:
            self.metodo_label.setText("Método: Não foi possível determinar")
            self.principio_label.setText("Princípio: Indefinido")

    def switch_to_previous(self):
        if self.stacked_widget.currentIndex() > 0:
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() - 1)

    def avancar(self):
        self.stacked_widget.setCurrentIndex(2)
