from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PySide6.QtWidgets import QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QMessageBox, QSizePolicy , QScrollArea
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QDate # Importar QDate para QDateEdit
from components.CustomRadioButton import CustomRadioButton # Se ainda for usar, mas QRadioButton padrão é suficiente aqui
from model.Session import Session # Assumindo que Session está em model/Session.py
import sqlite3 # Necessário para a função cadastrar_custo


class RegisterCostWindow(QWidget):
    def __init__(self, stacked_widget): # 
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self) # Define o layout principal diretamente no widget

        # --- Cabeçalho (similar ao da HomeWindow) ---
        header_layout = QHBoxLayout() 
        
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation) # Tamanho um pouco menor para o cabeçalho
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        
        header_layout.addStretch(1) # Empurra os elementos seguintes para a direita

        # Home Button (para voltar à tela inicial)
        home_button = QPushButton("Início")
        home_button.setObjectName("home_button")
        home_button.clicked.connect(lambda: self.switch_window_callback('home')) # Usa o callback
        header_layout.addWidget(home_button)

        sair_button = QPushButton("Sair") # Renomeado para sair_button para clareza
        sair_button.setObjectName("sair")
        sair_button.clicked.connect(self.logout_and_switch_to_welcome) # Nova função para logout
        header_layout.addWidget(sair_button)

        self.perfil_label = QLabel() # Renomeado para perfil_label para não confundir com a função perfil
        self.perfil_label.setObjectName("perfil")
        header_layout.addWidget(self.perfil_label)

        header_container = QWidget()
        header_container.setLayout(header_layout)
        main_layout.addWidget(header_container)

        # --- Linha Divisória ---
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        line1.setStyleSheet("color: #8faadc; background-color: #8faadc; height: 3px;")
        main_layout.addWidget(line1)

        # --- Título do Formulário ---
        form_title = QLabel("Registrar Novo Custo")
        form_title.setObjectName("form_title") # Para aplicar estilo via QSS
        form_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(form_title)

        # --- Formulário de Entrada ---
        form_container = QFrame()
        form_container.setObjectName("form_frame") # Para aplicar estilo ao frame do formulário
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15) # Espaçamento entre os campos do formulário
        form_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter) # Alinha o formulário ao topo e centraliza horizontalmente

        # Nome do Custo
        form_layout.addWidget(self.create_label_and_input("Nome do Custo:", "nome_custo", QLineEdit()))
        self.nome_custo_input = self.findChild(QLineEdit, "nome_custo_input") # Acessa o QLineEdit pelo objectName

        # Valor do Custo (usar QDoubleSpinBox para valores monetários)
        valor_widget = self.create_label_and_input("Valor do Custo:", "valor_custo", QDoubleSpinBox())
        self.valor_custo_input = valor_widget.findChild(QDoubleSpinBox, "valor_custo_input")
        self.valor_custo_input.setMinimum(0.00)
        self.valor_custo_input.setMaximum(999999999.99)
        self.valor_custo_input.setPrefix("R$ ")
        self.valor_custo_input.setDecimals(2)
        form_layout.addWidget(valor_widget, alignment=Qt.AlignCenter)

        # Data do Custo (usar QDateEdit para datas)
        data_widget = self.create_label_and_input("Data do Custo:", "data_custo", QDateEdit())
        self.data_custo_input = data_widget.findChild(QDateEdit, "data_custo_input")
        self.data_custo_input.setDate(QDate.currentDate()) # Data atual como padrão
        self.data_custo_input.setCalendarPopup(True) # Abrir calendário
        form_layout.addWidget(data_widget, alignment=Qt.AlignCenter)

        # Categoria do Custo (usar QComboBox para lista de opções)
        categoria_widget = self.create_label_and_input("Categoria do Custo:", "categoria_custo", QComboBox())
        self.categoria_custo_input = categoria_widget.findChild(QComboBox, "categoria_custo_input")
        self.categoria_custo_input.addItems(["Alimentação", "Transporte", "Moradia", "Lazer", "Educação", "Saúde", "Outros"])
        form_layout.addWidget(categoria_widget, alignment=Qt.AlignCenter)

        # É variável? (QRadioButton com texto claro)
        variavel_layout = QHBoxLayout()
        variavel_label = QLabel("Este custo é variável?")
        variavel_label.setObjectName("variavel_custo_label") 
        self.variavel_custo_radio = QRadioButton("Sim")
        self.variavel_custo_radio.setObjectName("variavel_custo_radio")
        variavel_layout.addWidget(variavel_label)
        variavel_layout.addWidget(self.variavel_custo_radio)
        variavel_layout.addStretch(1) 
        form_layout.addLayout(variavel_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Faz com que o conteúdo se ajuste

        scroll_widget = QWidget()
        scroll_widget.setLayout(form_layout)  # Põe o formulário dentro do widget de scroll

        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area, alignment=Qt.AlignCenter)
        # --- Botão de Cadastro ---
        cadastrar_button = QPushButton("Cadastrar Custo")
        cadastrar_button.setObjectName("cadastrar_button") # Para estilo
        cadastrar_button.clicked.connect(self.cadastrar_custo)
        
        # Centraliza o botão
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(cadastrar_button)
        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)


        main_layout.addStretch(1) # Empurra todo o conteúdo para o topo

        # --- Configurações Finais da Janela ---
        main_layout.setContentsMargins(30, 30, 30, 30) # Margens internas maiores
        main_layout.setSpacing(20) # Aumenta o espaçamento entre os blocos principais
        self.setLayout(main_layout)

    # --- Método auxiliar para criar labels e inputs ---
    def create_label_and_input(self, label_text, object_name_prefix, input_widget):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        label = QLabel(label_text)
        label.setObjectName(f"{object_name_prefix}_label") # Ex: "nome_custo_label"
        layout.addWidget(label, alignment=Qt.AlignCenter)
        
        input_widget.setObjectName(f"{object_name_prefix}_input") # Ex: "nome_custo_input"
        input_widget.setMinimumWidth(300) # Largura mínima para os inputs
        input_widget.setMaximumWidth(600) # Largura máxima para os inputs
        layout.addWidget(input_widget, alignment=Qt.AlignCenter) 
        
        return container

    def logout_and_switch_to_welcome(self):
        # Limpa a sessão ao sair
        Session.user_id = None
        Session.username = None
        # self.switch_window_callback('welcome') # Use o callback para ir para a Welcome (ou Login)
        self.stacked_widget.setCurrentIndex(0) # Volta para a tela de login (assumindo índice 0)


    def switch_to_welcome(self):
      
        self.stacked_widget.setCurrentIndex(2)

    def update_user_info(self):
        session = Session()

        username_display = session.username if session.username is not None else "Não Conectado"

        self.perfil_label.setText(f"Conectado: {username_display}")

    def cadastrar_custo(self):
        nome = self.nome_custo_input.text()
        valor = self.valor_custo_input.value() # Use .value() para QDoubleSpinBox
        data = self.data_custo_input.date().toString(Qt.ISODate) # Formato YYYY-MM-DD
        categoria = self.categoria_custo_input.currentText()
        is_variavel = self.variavel_custo_radio.isChecked()

        # Validação simples
        if not nome or valor <= 0:
            QMessageBox.warning(self, "Erro de Entrada", "Por favor, preencha o nome do custo e um valor válido.")
            return

        try:
            QMessageBox.information(self, "Custo Cadastrado", f"Custo '{nome}' cadastrado com sucesso!")

        except Exception as e:
            QMessageBox.critical(self, "Erro no Banco de Dados", f"Ocorreu um erro ao cadastrar o custo: {e}")