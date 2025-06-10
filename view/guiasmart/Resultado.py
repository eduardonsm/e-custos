from PySide6.QtWidgets import QFrame, QScrollArea, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton, QSizePolicy
from PySide6.QtGui import QPixmap, QCursor, QFont
from PySide6.QtCore import Qt

from model.Score import Score

class Resultado(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        # --- Layout Principal ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 5, 20, 20)
        layout.setSpacing(15)

        # --- Header ---
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

        # --- Linha Separadora ---
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        line1.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 2px;")
        layout.addWidget(line1)

        # --- Seção de Resultados ---
        main_container = QVBoxLayout()
        main_container.setSpacing(10)
        main_container.setContentsMargins(20, 10, 20, 20)
        
        pergunta = QLabel('Com base nas suas respostas, a recomendação é:')
        pergunta.setObjectName("pergunta")
        pergunta.setWordWrap(True)
        pergunta.setMinimumHeight(100)
        pergunta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_container.addWidget(pergunta, alignment=Qt.AlignmentFlag.AlignCenter)
        pergunta.setFont(QFont("Inter", 24, QFont.Bold))
        pergunta.setStyleSheet("font-size: 32px; font-weight: bold; color: #0f0b0b; padding: 15px;") # Preto

        # Labels que irão mostrar os resultados (iniciam vazios)
        self.metodo_label = QLabel("Método: -")
        self.metodo_label.setObjectName("resultado_metodo")
        self.metodo_label.setFont(QFont("Inter", 24, QFont.Bold))
        self.metodo_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #15803d; padding: 5px;") # Verde
        main_container.addWidget(self.metodo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.principio_label = QLabel("Princípio: -")
        self.principio_label.setObjectName("resultado_principio")
        self.principio_label.setFont(QFont("Inter", 24, QFont.Bold))
        self.principio_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #1d4ed8; padding: 5px;") # Azul
        main_container.addWidget(self.principio_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(main_container)
        layout.addStretch() # Adiciona espaço flexível para empurrar os botões para baixo

        # --- Linha Separadora ---
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        line2.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 2px;")
        layout.addWidget(line2)

        # --- Botões de Navegação ---
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
        """
        Esta função é chamada automaticamente toda vez que a tela (widget) se torna visível.
        É o lugar perfeito para carregar e exibir os resultados.
        """
        super().showEvent(event)
        self.carregar_e_exibir_resultados()

    def carregar_e_exibir_resultados(self):
        """
        Pega a instância do Score, calcula o resultado e atualiza os labels na tela.
        """
        score = Score()
        # Usei o nome do método do seu código original.
        # Ele deve retornar uma tupla com (metodo, principio)
        # Ex: ('RKW', 'Integral')
        resultado = score.SelecionarMetodoPrincipio()
        
        print("Respostas analisadas:", score.getRespostas())
        print("Resultado calculado:", resultado)

        if resultado and len(resultado) >= 2:
            metodo, principio = resultado[0], resultado[1]
            # Atualiza o texto dos labels que criamos no __init__
            self.metodo_label.setText(f"Método: {metodo}")
            self.principio_label.setText(f"Princípio: {principio}")
        else:
            # Caso algo dê errado no cálculo
            self.metodo_label.setText("Método: Não foi possível determinar")
            self.principio_label.setText("Princípio: Indefinido")

    def switch_to_previous(self):
        index = self.stacked_widget.currentIndex()
        if index > 0:
            self.stacked_widget.setCurrentIndex(index - 1)

    def avancar(self):
        # Aqui você pode colocar a lógica para ir para uma próxima tela
        # ou talvez fechar a aplicação. Removi o cálculo daqui.
        print("Botão 'Avançar/Finalizar' clicado!")
        index = self.stacked_widget.currentIndex()
        # Exemplo: self.stacked_widget.setCurrentIndex(index + 1)
        # ou self.window().close() para fechar
