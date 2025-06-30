from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup
from PySide6.QtWidgets import QLineEdit, QComboBox, QDoubleSpinBox, QMessageBox , QScrollArea
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from model.Session import Session
from viewModel.CostController import CostController

class RegisterCostWindow(QWidget):
    def __init__(self, stacked_widget): 
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
        form_title.setObjectName("pergunta")
        form_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(form_title)

        # --- Formulário de Entrada ---
        form_container = QFrame()
        form_container.setObjectName("form_frame") # Para aplicar estilo ao frame do formulário
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15) # Espaçamento entre os campos do formulário
        form_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter) # Alinha o formulário ao topo e centraliza horizontalmente

        # Nome do Custo
        nome_widget = self.create_label_and_input("Nome do Custo:", "nome_custo", QLineEdit())
        self.nome_custo_input = nome_widget.findChild(QLineEdit, "nome_custo_input") # Acessa o QLineEdit pelo objectName
        form_layout.addWidget(nome_widget)
        # Valor do Custo (usar QDoubleSpinBox para valores monetários)
        valor_widget = self.create_label_and_input("Valor do Custo:", "valor_custo", QDoubleSpinBox())
        self.valor_custo_input = valor_widget.findChild(QDoubleSpinBox, "valor_custo_input")
        self.valor_custo_input.setMinimum(0.00)
        self.valor_custo_input.setMaximum(999999999.99)
        self.valor_custo_input.setPrefix("R$ ")
        self.valor_custo_input.setDecimals(2)
        form_layout.addWidget(valor_widget)

        # Categoria do Custo (usar QComboBox para lista de opções)
        categoria_widget = self.create_label_and_input("Centro de Custo:", "categoria_custo", QComboBox())
        self.categoria_custo_input = categoria_widget.findChild(QComboBox, "categoria_custo_input")
        self.categoria_custo_input.addItems(["Alimentação", "Transporte", "Moradia", "Lazer", "Educação", "Saúde", "Outros"])
        form_layout.addWidget(categoria_widget)

        # Classificacao custo (variabilidade e alocaçao)
        variavel_layout = QHBoxLayout()
        direto_label = QLabel("Este custo é :")
        
        self.direto_radio = QRadioButton("Direto")
        self.direto_radio.setChecked(True)
        self.indireto_radio = QRadioButton("Indireto")
        diretoIndiretoGroup = QButtonGroup(self)
        diretoIndiretoGroup.addButton(self.direto_radio, 1)
        diretoIndiretoGroup.addButton(self.indireto_radio, 2)
        diretoIndiretoGroup.setExclusive(True)
        variavel_layout.addWidget(direto_label)
        variavel_layout.addWidget(self.direto_radio)
        variavel_layout.addWidget(self.indireto_radio)
        variavel_layout.addStretch(1) 

        variavel_label = QLabel("Este custo é :")
        self.fixo_radio = QRadioButton("Fixo")
        self.fixo_radio.setChecked(True)
        self.variavel_radio = QRadioButton("Variavel")
        fixoVariavelGroup = QButtonGroup(self)
        fixoVariavelGroup.addButton(self.fixo_radio, 1)
        fixoVariavelGroup.addButton(self.variavel_radio, 2)
        fixoVariavelGroup.setExclusive(True)
        
        variavel_layout.addWidget(variavel_label)
        variavel_layout.addWidget(self.fixo_radio)
        variavel_layout.addWidget(self.variavel_radio)
        variavel_layout.addStretch(1) 

        form_layout.addLayout(variavel_layout)

        # Classificacao custo (tomada de decisao e eliminacao)
        classificacao2_layout = QHBoxLayout()
        label = QLabel("Este custo é :")
        
        self.relevante_radio = QRadioButton("Relevante")
        self.relevante_radio.setChecked(True)
        self.naorelevante_radio = QRadioButton("Nao Relevante")
        relevanciaGroup = QButtonGroup(self)
        relevanciaGroup.addButton(self.relevante_radio, 1)
        relevanciaGroup.addButton(self.naorelevante_radio, 2)
        relevanciaGroup.setExclusive(True)
        classificacao2_layout.addWidget(label)
        classificacao2_layout.addWidget(self.relevante_radio)
        classificacao2_layout.addWidget(self.naorelevante_radio)
        classificacao2_layout.addStretch(1) 

        label = QLabel("Este custo é :")
        self.eliminavel_radio = QRadioButton("Eliminavel")
        self.eliminavel_radio.setChecked(True)
        self.naoEliminavel_radio = QRadioButton("Nao Eliminavel")
        eliminavelnaoEliminavelGroup = QButtonGroup(self)
        eliminavelnaoEliminavelGroup.addButton(self.eliminavel_radio, 1)
        eliminavelnaoEliminavelGroup.addButton(self.naoEliminavel_radio, 2)
        eliminavelnaoEliminavelGroup.setExclusive(True)
        classificacao2_layout.addWidget(label)
        classificacao2_layout.addWidget(self.eliminavel_radio)
        classificacao2_layout.addWidget(self.naoEliminavel_radio)
        classificacao2_layout.addStretch(1) 
        form_layout.addLayout(classificacao2_layout)

        # Classificacao custo (oculto)
        classificacao3_layout = QHBoxLayout()
        label = QLabel("Este custo é :")
        
        self.oculto_radio = QRadioButton("Oculto")
        self.oculto_radio.setChecked(True)
        self.naooculto_radio = QRadioButton("Nao Oculto")
        ocultoGroup = QButtonGroup(self)
        ocultoGroup.addButton(self.oculto_radio, 1)
        ocultoGroup.addButton(self.naooculto_radio, 2)
        ocultoGroup.setExclusive(True)
        classificacao3_layout.addWidget(label)
        classificacao3_layout.addWidget(self.oculto_radio)
        classificacao3_layout.addWidget(self.naooculto_radio)
        classificacao3_layout.addStretch(1) 

        form_layout.addLayout(classificacao3_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Faz com que o conteúdo se ajuste

        scroll_widget = QWidget()
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)
        # --- Botão de Cadastro ---
        cadastrar_button = QPushButton("Cadastrar Custo")
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
        layout.addWidget(label)
        
        input_widget.setObjectName(f"{object_name_prefix}_input") # Ex: "nome_custo_input"
        input_widget.setMinimumWidth(300) # Largura mínima para os inputs
        input_widget.setMaximumWidth(600) # Largura máxima para os inputs
        layout.addWidget(input_widget) 
        
        return container

    def logout_and_switch_to_welcome(self):
        # Limpa a sessão ao sair
        Session.user_id = None
        Session.username = None
        self.stacked_widget.setCurrentIndex(0) # Volta para a tela de login (assumindo índice 0)


    def switch_to_welcome(self):
      
        self.stacked_widget.setCurrentIndex(2)

    def update_user_info(self):
        session = Session()

        username_display = session.username if session.username is not None else "Não Conectado"

        self.perfil_label.setText(f"Conectado: {username_display}")

    
    def cadastrar_custo(self):
        """
            nome
            valor
            categoria (centro de custo?)
            variabilidade
            alocacao
            tomada de decisao
            eliminavel
            oculto
        """
        nome = self.nome_custo_input.text()
        valor = self.valor_custo_input.value() 
        categoria = self.categoria_custo_input.currentText()
        is_direto = self.direto_radio.isChecked()
        is_fixo = self.fixo_radio.isChecked()
        is_relevante = self.relevante_radio.isChecked()
        is_eliminavel = self.eliminavel_radio.isChecked()
        is_oculto = self.oculto_radio.isChecked()

        
        # Validação simples
        if not nome or valor <= 0:
            QMessageBox.warning(self, "Erro de Entrada", "Por favor, preencha o nome do custo e um valor válido.")
            return

        try:
            session = Session()
            id = session.user_id
            costController = CostController()
            costController.add_cost_to_db(nome, valor, categoria, is_direto, is_fixo, is_relevante, is_eliminavel, is_oculto, id)

            print(f"Registrando custo: {nome}, Valor: {valor}, Categoria: {categoria}, Direto: {is_direto}, Fixo: {is_fixo}, Relevante: {is_relevante}, Eliminável: {is_eliminavel}, Oculto: {is_oculto}")
            QMessageBox.information(self, "Sucesso", "Custo cadastrado com sucesso!")
            self.stacked_widget.setCurrentIndex(29)

        except Exception as e:
            QMessageBox.critical(self, "Erro no Banco de Dados", f"Ocorreu um erro ao cadastrar o custo: {e}")