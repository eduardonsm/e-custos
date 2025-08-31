# Adicione QComboBox aos imports do QtWidgets
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QLineEdit, QFrame, QComboBox,
                               QDoubleSpinBox, QSpinBox, QMessageBox, QScrollArea,
                               QFormLayout)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from model.Session import Session
from model.MaoDeObraDireta import MaoDeObraDireta
from model.MaoDeObraDiretaRepository import MaoDeObraDiretaRepository
# Importe também o repositório de Centro de Custo para buscar os dados
from model.CentroCustoRepository import CentroCustoRepository

class RegisterMaoDeObraDiretaWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.mod_repo = MaoDeObraDiretaRepository()
        # 1. Instancie o repositório de Centro de Custo
        self.centro_custo_repo = CentroCustoRepository()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Cabeçalho e Divisória (sem alterações) ---
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
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # --- Título (sem alterações) ---
        title = QLabel("Cadastro de Mão de Obra Direta")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        # --- Formulário (com o QLineEdit trocado por QComboBox) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(15)

        self.lbl_id = QLabel("Novo")
        form_layout.addRow("ID:", self.lbl_id)

        self.txt_cargo = QLineEdit()
        self.txt_cargo.setPlaceholderText("Ex: Operador de Máquina CNC")
        form_layout.addRow("Cargo:", self.txt_cargo)

        # 2. Troque o QLineEdit por um QComboBox
        self.combo_centro_custo = QComboBox()
        form_layout.addRow("Centro de Custo:", self.combo_centro_custo)

        self.txt_operacao = QLineEdit()
        self.txt_operacao.setPlaceholderText("Ex: Tornear Peça X")
        form_layout.addRow("Operação:", self.txt_operacao)

        # --- Restante do formulário (sem alterações) ---
        self.spin_tempo_padrao = QDoubleSpinBox()
        self.spin_tempo_padrao.setSuffix(" h")
        self.spin_tempo_padrao.setDecimals(4)
        self.spin_tempo_padrao.setMaximum(9999.9999)
        form_layout.addRow("Tempo Padrão:", self.spin_tempo_padrao)

        self.spin_capacidade_horas = QDoubleSpinBox()
        self.spin_capacidade_horas.setSuffix(" h/mês")
        self.spin_capacidade_horas.setDecimals(2)
        self.spin_capacidade_horas.setMaximum(99999.99)
        form_layout.addRow("Capacidade (Horas):", self.spin_capacidade_horas)
        
        self.spin_capacidade_itens = QSpinBox()
        self.spin_capacidade_itens.setSuffix(" un/mês")
        self.spin_capacidade_itens.setMaximum(999999)
        form_layout.addRow("Capacidade (Itens):", self.spin_capacidade_itens)
        
        self.spin_custo_hora = QDoubleSpinBox()
        self.spin_custo_hora.setPrefix("R$ ")
        self.spin_custo_hora.setDecimals(2)
        self.spin_custo_hora.setMaximum(9999.99)
        form_layout.addRow("Custo por Hora:", self.spin_custo_hora)

        scroll.setWidget(form_container)
        main_layout.addWidget(scroll)

        # --- Botões (sem alterações) ---
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar Mão de Obra")
        btn_salvar.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_salvar.clicked.connect(self.salvar_mod)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #f44336; color: white;")
        btn_cancelar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(29))
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_salvar)
        main_layout.addLayout(btn_layout)

    # 3. Crie um método para carregar os dados na view
    def load_view_data(self):
        """Carrega dados dinâmicos, como o nome do usuário e a lista de centros de custo."""
        self.update_user_info()
        self.popular_centros_custo()

    def popular_centros_custo(self):
        """Busca os centros de custo no banco e os adiciona ao QComboBox."""
        self.combo_centro_custo.clear()
        try:
            user_id = Session().user_id
            if user_id:
                centros = self.centro_custo_repo.get_centros_by_user(user_id)
                self.combo_centro_custo.addItem("Selecione um Centro de Custo")
                for centro in centros:
                    self.combo_centro_custo.addItem(centro.descricao)
        except Exception as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Não foi possível carregar os centros de custo:\n{e}")


    def logout_and_switch_to_welcome(self):
        Session().clear_session()
        self.stacked_widget.setCurrentIndex(29)

    def update_user_info(self):
        session = Session()
        username = session.username if session.username else "Não conectado"
        self.perfil_label.setText(f"Usuário: {username}")

    def salvar_mod(self):
        # 4. Ajuste a validação e a obtenção de dados para o QComboBox
        if not self.txt_cargo.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe o cargo!")
            return
        # Valida se uma opção válida foi selecionada no ComboBox
        if self.combo_centro_custo.currentIndex() <= 0:
            QMessageBox.warning(self, "Atenção", "Selecione um centro de custo!")
            return

        try:
            mod = MaoDeObraDireta(
                cargo=self.txt_cargo.text(),
                # Pega o texto do item selecionado no ComboBox
                centro_custo=self.combo_centro_custo.currentText(),
                operacao=self.txt_operacao.text(),
                tempo_padrao=self.spin_tempo_padrao.value(),
                capacidade_horas=self.spin_capacidade_horas.value(),
                capacidade_itens=self.spin_capacidade_itens.value(),
                custo_hora=self.spin_custo_hora.value(),
                user_id=Session().user_id
            )

            self.mod_repo.add_mod(mod)
            QMessageBox.information(self, "Sucesso", "Mão de Obra cadastrada com sucesso!")
            self.limpar_formulario()
            self.stacked_widget.setCurrentIndex(29)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao cadastrar Mão de Obra:\n{str(e)}")

    def limpar_formulario(self):
        """Reseta todos os campos do formulário para o estado inicial"""
        self.lbl_id.setText("Novo")
        self.txt_cargo.clear()
        # 5. Ajuste o método de limpar para resetar o QComboBox
        self.combo_centro_custo.setCurrentIndex(0)
        self.txt_operacao.clear()
        self.spin_tempo_padrao.setValue(0)
        self.spin_capacidade_horas.setValue(0)
        self.spin_capacidade_itens.setValue(0)
        self.spin_custo_hora.setValue(0)