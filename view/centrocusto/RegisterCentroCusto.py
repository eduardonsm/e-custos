from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QLineEdit, QFrame, QRadioButton,
                               QDoubleSpinBox, QSpinBox, QMessageBox, QScrollArea,
                               QFormLayout, QGroupBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from model.Session import Session
from model.CentroCusto import CentroCusto  # Importa o modelo correto
from model.CentroCustoRepository import CentroCustoRepository  # Importa o repositório correto

class RegisterCentroCustoWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        # Instancia o repositório de Centro de Custo
        self.centro_custo_repo = CentroCustoRepository()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Cabeçalho (Mantido igual) ---
        header_layout = QHBoxLayout()
        
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        
        header_layout.addStretch(1)

        home_button = QPushButton("Início")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        header_layout.addWidget(home_button)

        sair_button = QPushButton("Sair")
        sair_button.clicked.connect(self.logout_and_switch_to_welcome)
        header_layout.addWidget(sair_button)

        self.perfil_label = QLabel()
        header_layout.addWidget(self.perfil_label)

        main_layout.addLayout(header_layout)

        # --- Divisória (Mantida igual) ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # --- Título (Alterado) ---
        title = QLabel("Cadastro de Centros de Custo")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        # --- Formulário (Scroll Area - Adaptado para Centro de Custo) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(15)

        # ID (somente exibição)
        self.lbl_id = QLabel("Novo")
        form_layout.addRow("ID:", self.lbl_id)

        # Descrição
        self.txt_descricao = QLineEdit()
        self.txt_descricao.setPlaceholderText("Ex: Usinagem, Montagem, Almoxarifado...")
        form_layout.addRow("Descrição:", self.txt_descricao)

        # Tipo (Rádio buttons)
        tipo_group = QGroupBox("Tipo de Centro de Custo")
        tipo_layout = QHBoxLayout()
        self.radio_produtivo = QRadioButton("Produtivo")
        self.radio_auxiliar = QRadioButton("Auxiliar")
        self.radio_administrativo = QRadioButton("Administrativo")
        self.radio_produtivo.setChecked(True)
        
        tipo_layout.addWidget(self.radio_produtivo)
        tipo_layout.addWidget(self.radio_auxiliar)
        tipo_layout.addWidget(self.radio_administrativo)
        tipo_group.setLayout(tipo_layout)
        form_layout.addRow(tipo_group)

        # Quantidade de Postos
        self.spin_postos = QSpinBox()
        self.spin_postos.setMinimum(1)
        self.spin_postos.setMaximum(9999)
        form_layout.addRow("Quantidade de Postos:", self.spin_postos)

        # Capacidade em Horas
        self.spin_capacidade_horas = QDoubleSpinBox()
        self.spin_capacidade_horas.setSuffix(" h/mês")
        self.spin_capacidade_horas.setDecimals(2)
        self.spin_capacidade_horas.setMaximum(99999.99)
        form_layout.addRow("Capacidade (Horas):", self.spin_capacidade_horas)
        
        # Capacidade em Itens
        self.spin_capacidade_itens = QSpinBox()
        self.spin_capacidade_itens.setSuffix(" un/mês")
        self.spin_capacidade_itens.setMaximum(999999)
        form_layout.addRow("Capacidade (Itens):", self.spin_capacidade_itens)

        scroll.setWidget(form_container)
        main_layout.addWidget(scroll)

        # --- Botões (Texto do botão Salvar alterado) ---
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar Centro de Custo")
        btn_salvar.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_salvar.clicked.connect(self.salvar_centro_custo)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #f44336; color: white;")
        btn_cancelar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_salvar)
        main_layout.addLayout(btn_layout)

    def logout_and_switch_to_welcome(self):
        Session().clear_session()
        self.stacked_widget.setCurrentIndex(0)

    def update_user_info(self):
        session = Session()
        username = session.username if session.username else "Não conectado"
        self.perfil_label.setText(f"Usuário: {username}")

    def salvar_centro_custo(self):
        # Validação básica
        if not self.txt_descricao.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe a descrição do centro de custo!")
            return

        try:
            # Obter dados do formulário
            tipo = ""
            if self.radio_produtivo.isChecked():
                tipo = "Produtivo"
            elif self.radio_auxiliar.isChecked():
                tipo = "Auxiliar"
            else:
                tipo = "Administrativo"
            
            centro = CentroCusto(
                descricao=self.txt_descricao.text(),
                tipo=tipo,
                quantidade_postos=self.spin_postos.value(),
                capacidade_horas=self.spin_capacidade_horas.value(),
                capacidade_itens=self.spin_capacidade_itens.value(),
                user_id=Session().user_id
            )

            self.centro_custo_repo.add_centro_custo(centro)
            
            QMessageBox.information(self, "Sucesso", "Centro de custo cadastrado com sucesso!")
            self.limpar_formulario()
            self.stacked_widget.setCurrentIndex(29)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao cadastrar centro de custo:\n{str(e)}")

    def limpar_formulario(self):
        """Reseta todos os campos do formulário"""
        self.lbl_id.setText("Novo")
        self.txt_descricao.clear()
        self.radio_produtivo.setChecked(True)
        self.spin_postos.setValue(1)
        self.spin_capacidade_horas.setValue(0)
        self.spin_capacidade_itens.setValue(0)