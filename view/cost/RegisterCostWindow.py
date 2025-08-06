from PySide6.QtWidgets import (QFrame, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, 
                               QLabel, QPushButton, QButtonGroup, QLineEdit, QComboBox, 
                               QDoubleSpinBox, QMessageBox, QScrollArea, QSpinBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from model.Session import Session
from viewModel.CostController import CostController
from viewModel.ProductController import ProductController

class RegisterCostWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.cost_controller = CostController()
        self.product_controller = ProductController()
        self.products_list = [] # Guardará a lista de objetos Product
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Cabeçalho ---
        header_layout = QHBoxLayout()
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        header_layout.addStretch(1)

        home_button = QPushButton("Início")
        home_button.setObjectName("home_button")
        # Conecte o botão home à sua função correspondente, se necessário
        # home_button.clicked.connect(self.switch_to_home) 
        header_layout.addWidget(home_button)

        sair_button = QPushButton("Sair")
        sair_button.setObjectName("sair")
        sair_button.clicked.connect(self.logout_and_switch_to_welcome)
        header_layout.addWidget(sair_button)

        self.perfil_label = QLabel()
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
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15)
        form_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # --- Novos Inputs ---
        
        # Código do Custo (code)
        code_widget = self.create_label_and_input("Código do Custo:", "code", QLineEdit())
        self.code_input = code_widget.findChild(QLineEdit, "code_input")
        form_layout.addWidget(code_widget)

        # Produto (product) - Idealmente, preenchido a partir do banco de dados
        product_widget = self.create_label_and_input("Produto Associado:", "product", QComboBox())
        self.product_input = product_widget.findChild(QComboBox, "product_input")
                
        form_layout.addWidget(product_widget)
        
        # Descrição (description)
        description_widget = self.create_label_and_input("Descrição do Custo:", "description", QLineEdit())
        self.description_input = description_widget.findChild(QLineEdit, "description_input")
        form_layout.addWidget(description_widget)

        # Quantidade (quantity)
        quantity_widget = self.create_label_and_input("Quantidade:", "quantity", QSpinBox())
        self.quantity_input = quantity_widget.findChild(QSpinBox, "quantity_input")
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(999999)
        form_layout.addWidget(quantity_widget)

        # Preço Unitário (unitPrice)
        unit_price_widget = self.create_label_and_input("Preço Unitário:", "unit_price", QDoubleSpinBox())
        self.unit_price_input = unit_price_widget.findChild(QDoubleSpinBox, "unit_price_input")
        self.unit_price_input.setMinimum(0.00)
        self.unit_price_input.setMaximum(999999999.99)
        self.unit_price_input.setPrefix("R$ ")
        self.unit_price_input.setDecimals(2)
        form_layout.addWidget(unit_price_widget)

        # --- Classificações (Radio Buttons) ---
        
        # Alocação (Direto/Indireto) e Variabilidade (Fixo/Variável)
        classification1_layout = QHBoxLayout()
        classification1_layout.addWidget(QLabel("Alocação:"))
        self.direto_radio = QRadioButton("Direto")
        self.indireto_radio = QRadioButton("Indireto")
        self.direto_radio.setChecked(True)
        self.alocacao_group = QButtonGroup(self)
        self.alocacao_group.addButton(self.direto_radio)
        self.alocacao_group.addButton(self.indireto_radio)
        classification1_layout.addWidget(self.direto_radio)
        classification1_layout.addWidget(self.indireto_radio)
        classification1_layout.addStretch(1)

        classification1_layout.addWidget(QLabel("Variabilidade:"))
        self.fixo_radio = QRadioButton("Fixo")
        self.variavel_radio = QRadioButton("Variável")
        self.fixo_radio.setChecked(True)
        self.variabilidade_group = QButtonGroup(self)
        self.variabilidade_group.addButton(self.fixo_radio)
        self.variabilidade_group.addButton(self.variavel_radio)
        classification1_layout.addWidget(self.fixo_radio)
        classification1_layout.addWidget(self.variavel_radio)
        classification1_layout.addStretch(1)
        form_layout.addLayout(classification1_layout)

        # Tomada de Decisão (Relevante/Não Relevante) e Eliminável
        classification2_layout = QHBoxLayout()
        classification2_layout.addWidget(QLabel("Decisão:"))
        self.relevante_radio = QRadioButton("Relevante")
        self.naorelevante_radio = QRadioButton("Não Relevante")
        self.relevante_radio.setChecked(True)
        self.relevancia_group = QButtonGroup(self)
        self.relevancia_group.addButton(self.relevante_radio)
        self.relevancia_group.addButton(self.naorelevante_radio)
        classification2_layout.addWidget(self.relevante_radio)
        classification2_layout.addWidget(self.naorelevante_radio)
        classification2_layout.addStretch(1)
        
        classification2_layout.addWidget(QLabel("Eliminável:"))
        self.eliminavel_radio = QRadioButton("Eliminável")
        self.naoEliminavel_radio = QRadioButton("Não Eliminável")
        self.eliminavel_radio.setChecked(True)
        self.eliminavel_group = QButtonGroup(self)
        self.eliminavel_group.addButton(self.eliminavel_radio)
        self.eliminavel_group.addButton(self.naoEliminavel_radio)
        classification2_layout.addWidget(self.eliminavel_radio)
        classification2_layout.addWidget(self.naoEliminavel_radio)
        classification2_layout.addStretch(1)
        form_layout.addLayout(classification2_layout)

        # Oculto
        classification3_layout = QHBoxLayout()
        classification3_layout.addWidget(QLabel("Controle:"))
        self.oculto_radio = QRadioButton("Oculto")
        self.naooculto_radio = QRadioButton("Não Oculto")
        self.naooculto_radio.setChecked(True) # O padrão geralmente é "Não Oculto"
        self.oculto_group = QButtonGroup(self)
        self.oculto_group.addButton(self.oculto_radio)
        self.oculto_group.addButton(self.naooculto_radio)
        classification3_layout.addWidget(self.oculto_radio)
        classification3_layout.addWidget(self.naooculto_radio)
        classification3_layout.addStretch(1)
        form_layout.addLayout(classification3_layout)

        # --- Scroll Area ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(form_container)
        main_layout.addWidget(scroll_area)

        # --- Botão de Cadastro ---
        cadastrar_button = QPushButton("Cadastrar Custo")
        cadastrar_button.clicked.connect(self.cadastrar_custo)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(cadastrar_button)
        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        main_layout.addStretch(1)
        self.setLayout(main_layout)

    def create_label_and_input(self, label_text, object_name_prefix, input_widget):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(label_text)
        label.setObjectName(f"{object_name_prefix}_label")
        layout.addWidget(label)
        
        input_widget.setObjectName(f"{object_name_prefix}_input")
        input_widget.setMinimumWidth(300)
        input_widget.setMaximumWidth(600)
        layout.addWidget(input_widget)
        
        return container

    def load_products(self):
        """Busca os produtos do usuário logado e popula o QComboBox."""
        self.product_input.clear()
        self.products_list.clear()
        
        user_id = Session().user_id
        if not user_id:
            print("Nenhum usuário logado para carregar produtos.")
            return

        try:
            self.products_list = self.product_controller.get_products_by_user(user_id)
            if not self.products_list:
                self.product_input.addItem("Nenhum produto cadastrado")
                self.product_input.setEnabled(False)
            else:
                self.product_input.setEnabled(True)
                for product in self.products_list:
                    self.product_input.addItem(product.name) # Adiciona apenas o nome
        except Exception as e:
            QMessageBox.critical(self, "Erro ao Carregar Produtos", f"Não foi possível carregar a lista de produtos: {e}")

    ### 5. Novo método para ser chamado sempre que a tela for exibida ###
    def refresh_data(self):
        """Atualiza todas as informações dinâmicas da tela."""
        self.update_user_info()
        self.load_products()

    def cadastrar_custo(self):
        try:
            ### 6. Lógica atualizada para obter o ID do produto selecionado ###
            selected_index = self.product_input.currentIndex()
            
            # Valida se um produto válido foi selecionado
            if selected_index == -1 or not self.products_list:
                QMessageBox.warning(self, "Erro de Entrada", "Por favor, selecione um produto válido.")
                return

            # Pega o objeto Product completo da nossa lista e extrai o ID
            selected_product = self.products_list[selected_index]
            product_id = selected_product.id
            
            # Coleta dos outros dados da UI (continua igual)
            code_str = self.code_input.text()
            description = self.description_input.text()
            quantity = self.quantity_input.value()
            unit_price = self.unit_price_input.value()
            is_fixo = self.fixo_radio.isChecked()
            is_direto = self.direto_radio.isChecked()
            is_relevante = self.relevante_radio.isChecked()
            is_eliminavel = self.eliminavel_radio.isChecked()
            is_oculto = self.oculto_radio.isChecked()
            user_id = Session().user_id

            # Validação (continua igual)
            if not code_str or not description or quantity <= 0 or unit_price <= 0:
                QMessageBox.warning(self, "Erro de Entrada", "Preencha todos os campos obrigatórios com valores válidos.")
                return
            
            code = int(code_str)

            # Chamada ao Controller (continua igual)
            success = self.cost_controller.add_cost(
                code, product_id, description, quantity, unit_price,
                is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto,
                user_id
            )

            if success:
                QMessageBox.information(self, "Sucesso", "Custo cadastrado com sucesso!")
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível cadastrar o custo.")

        except ValueError:
             QMessageBox.warning(self, "Erro de Entrada", "O código do custo deve ser um número inteiro.")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", f"Ocorreu um erro ao cadastrar o custo: {e}")
    
    def update_user_info(self):
        session = Session()
        username_display = session.username if session.username is not None else "Não Conectado"
        self.perfil_label.setText(f"Conectado: {username_display}")

    def logout_and_switch_to_welcome(self):
        Session.user_id = None
        Session.username = None
        self.stacked_widget.setCurrentIndex(0)