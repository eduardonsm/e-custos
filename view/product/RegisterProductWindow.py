import json
from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup
from PySide6.QtWidgets import QLineEdit, QDoubleSpinBox, QMessageBox , QScrollArea, QDateEdit

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from model.Session import Session
from viewModel.ProductController import ProductController

class RegisterProductWindow(QWidget):
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
        form_title = QLabel("Registrar Novo Produto")
        form_title.setObjectName("pergunta")
        form_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(form_title)

        # --- Formulário de Entrada ---
        form_container = QFrame()
        form_container.setObjectName("form_frame") # Para aplicar estilo ao frame do formulário
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15) # Espaçamento entre os campos do formulário
        form_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter) # Alinha o formulário ao topo e centraliza horizontalmente

        # Nome do Produto
        nome_widget = self.create_label_and_input("Nome do Produto:", "nome_produto", QLineEdit())
        self.nome_produto_input = nome_widget.findChild(QLineEdit, "nome_produto_input") # Acessa o QLineEdit pelo objectName
        form_layout.addWidget(nome_widget)
        # Valor do Produto (usar QDoubleSpinBox para valores monetários)
        valor_widget = self.create_label_and_input("Valor do Produto:", "valor_produto", QDoubleSpinBox())
        self.valor_produto_input = valor_widget.findChild(QDoubleSpinBox, "valor_produto_input")
        self.valor_produto_input.setMinimum(0.00)
        self.valor_produto_input.setMaximum(999999999.99)
        self.valor_produto_input.setPrefix("R$ ")
        self.valor_produto_input.setDecimals(2)
        form_layout.addWidget(valor_widget)
        # Data do Projeto
        data_projeto_widget = self.create_label_and_input("Data do Projeto:", "data_projeto", QDateEdit())
        self.data_projeto_input = data_projeto_widget.findChild(QDateEdit, "data_projeto_input")
        self.data_projeto_input.setCalendarPopup(True)
        form_layout.addWidget(data_projeto_widget)
        # Data de Início
        data_inicio_widget = self.create_label_and_input("Data de Início:", "data_inicio", QDateEdit())
        self.data_inicio_input = data_inicio_widget.findChild(QDateEdit, "data_inicio_input")
        self.data_inicio_input.setCalendarPopup(True)
        form_layout.addWidget(data_inicio_widget)
       

        active_layout = QHBoxLayout()
        active_label = QLabel("Este produto está :")
        self.ativo_radio = QRadioButton("Ativo")
        self.ativo_radio.setChecked(True)
        self.inativo_radio = QRadioButton("Inativo")
        ativoInativoGroup = QButtonGroup(self)
        ativoInativoGroup.addButton(self.ativo_radio, 1)
        ativoInativoGroup.addButton(self.inativo_radio, 2)
        ativoInativoGroup.setExclusive(True)
        active_layout.addWidget(active_label)
        active_layout.addWidget(self.ativo_radio)
        active_layout.addWidget(self.inativo_radio)
        active_layout.addStretch(1) 

        if self.ativo_radio.isChecked():
             # Data de Fim
            data_fim_widget = self.create_label_and_input("Data de Fim:", "data_fim", QDateEdit())
            self.data_fim_input = data_fim_widget.findChild(QDateEdit, "data_fim_input")
            self.data_fim_input.setCalendarPopup(True)
            form_layout.addWidget(data_fim_widget)
        
        else:
            self.data_fim_input = QDateEdit()
            self.data_fim_input.setEnabled(False)

        form_layout.addWidget(self.data_fim_input)
        form_layout.addLayout(active_layout)
                # --- Árvore do Produto ---
        arvore_label = QLabel("Árvore do Produto (Componentes e Quantidades):")
        arvore_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(arvore_label)

        self.componente_inputs = []  # Guardará pares (nome_input, qtd_input)

        def add_componente_input(nome='', qtd=1):
            componente_widget = QWidget()
            componente_layout = QHBoxLayout(componente_widget)

            nome_input = QLineEdit()
            nome_input.setPlaceholderText("Nome do componente")
            nome_input.setText(nome)
            qtd_input = QDoubleSpinBox()
            qtd_input.setMinimum(0.01)
            qtd_input.setValue(qtd)
            qtd_input.setSuffix(" un.")
            qtd_input.setMaximum(100000)

            remover_btn = QPushButton("Remover")
            remover_btn.clicked.connect(lambda: remove_componente_input(componente_widget))

            componente_layout.addWidget(nome_input)
            componente_layout.addWidget(qtd_input)
            componente_layout.addWidget(remover_btn)

            self.componente_inputs.append((nome_input, qtd_input))
            form_layout.addWidget(componente_widget)

        def remove_componente_input(widget):
            for i, (nome_input, qtd_input) in enumerate(self.componente_inputs):
                if widget.findChild(QLineEdit) == nome_input:
                    self.componente_inputs.pop(i)
                    break
            widget.setParent(None)

        add_btn = QPushButton("Adicionar Componente")
        add_btn.clicked.connect(lambda: add_componente_input())
        form_layout.addWidget(add_btn)

        # Adiciona um componente por padrão
        add_componente_input()


        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Faz com que o conteúdo se ajuste

        scroll_widget = QWidget()
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)
        # --- Botão de Cadastro ---
        cadastrar_button = QPushButton("Cadastrar Produto")
        cadastrar_button.clicked.connect(self.cadastrar_produto)
        
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
 
    def cadastrar_produto(self):
        """
        name
        dateProject
        dateStart
        isActive
        endTime
        valor
        productTree
        """
        name = self.nome_produto_input.text()
        dateProject = self.data_projeto_input.date().toString("yyyy-MM-dd")
        dateStart = self.data_inicio_input.date().toString("yyyy-MM-dd")
        isActive = self.ativo_radio.isChecked()
        endTime = self.data_fim_input.date().toString("yyyy-MM-dd")
        valor = self.valor_produto_input.value()
        productTree = json.dumps([
            {"nome": nome_input.text(), "quantidade": qtd_input.value()}
            for nome_input, qtd_input in self.componente_inputs
            if nome_input.text().strip() != ''
        ])

        
        # Validação simples
        if not name or valor <= 0:
            QMessageBox.warning(self, "Erro de Entrada", "Por favor, preencha o nome do produto e um valor válido.")
            return

        try:
            session = Session()
            id = session.user_id
            productController = ProductController()
            productController.add_product(name, dateProject, dateStart, isActive, endTime, valor, productTree, id)

            print(f"Registrando produto: {name}, Data do Projeto: {dateProject}, Data de Início: {dateStart}, Ativo: {isActive}, Data de Fim: {endTime}, Preço: {valor}, ProductTree: {productTree}")
            QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso!")
            self.stacked_widget.setCurrentIndex(29)

        except Exception as e:
            QMessageBox.critical(self, "Erro no Banco de Dados", f"Ocorreu um erro ao cadastrar o produto: {e}")