from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QScrollArea, QGroupBox, QGridLayout)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class HomeWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 5)
        main_layout.setSpacing(10)

        # --- Cabeçalho ---
        header = QHBoxLayout()
        
        # Logo
        logo = QLabel()
        logo.setPixmap(QPixmap("./images/ecustos-logo.png").scaled(120, 120, Qt.KeepAspectRatio))
        header.addWidget(logo)
        
        header.addStretch()
        
        # Botões do cabeçalho
        header.addWidget(QPushButton("Gerar Relatório"))
        btn_sair = QPushButton("Sair")
        btn_sair.clicked.connect(self.switch_to_login)
        header.addWidget(btn_sair)
        self.perfil = QLabel("Usuário")
        header.addWidget(self.perfil)

        main_layout.addLayout(header)

        # --- Área rolável com GRID FUNCIONAL ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        grid = QGridLayout(content)
        
        # Botões com métodos conectados
        buttons = [
            ("Cadastrar Produtos", self.cadastrar_produtos),
            ("BOM/Cadastrar item", self.bom_cadastrar),
            ("Materiais diretos", self.materiais_diretos),
            ("MOD", self.mod),
            ("Centros de custos", self.centros_custo),
            ("Recursos produtivos", self.recursos_produtivos),
            ("CIF", self.cif),
            ("Custo ocultos", self.custo_ocultos),
            ("Processos", self.processos),
            ("Bases de rateio", self.bases_rateio),
            ("Visualizar cadastro", self.visualizar_cadastro)
        ]
        
        for i, (text, callback) in enumerate(buttons):
            btn = QPushButton(text)
            btn.setMinimumHeight(50)
            btn.clicked.connect(callback)
            grid.addWidget(btn, i//3, i%3)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # --- Menu Inferior FIXO ---
        menu = QHBoxLayout()
        menu.setSpacing(15)        
        
        menu_items = [
            ("Cadastros", self.menu_cadastros),
            ("Operações", self.menu_operacoes),
            ("Análises", self.menu_analises),
            ("Métodos", self.menu_metodos),
            ("Princípios", self.menu_principios),
            ("Desperdícios", self.menu_desperdicios),
            ("Configurações", self.menu_configuracoes),
            ("Relatórios", self.menu_relatorios)
        ]
        
        for text, callback in menu_items:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            menu.addWidget(btn)
        
        main_layout.addLayout(menu)

    # --- Todos os métodos conectados ---
    
    # Métodos da grid principal
    def bom_cadastrar(self):  self.switch_to_screen(32)
    def cadastrar_produtos(self): self.switch_to_screen(31)
    def visualizar_lista(self): print("Visualizar lista chamado")
    def materiais_diretos(self): self.switch_to_screen(31)
    def mod(self): self.switch_to_screen(32)
    def centros_custo(self): self.switch_to_screen(34)
    def recursos_produtivos(self): self.switch_to_screen(34)
    def cif(self): self.switch_to_screen(35)
    def custo_ocultos(self): self.switch_to_screen(36)
    def processos(self): self.switch_to_screen(37)
    def bases_rateio(self): self.switch_to_screen(38)
    def visualizar_cadastro(self): self.switch_to_screen(39)
    
    # Métodos do menu inferior
    def menu_cadastros(self): self.switch_to_screen(40)
    def menu_operacoes(self): self.switch_to_screen(41)
    def menu_analises(self): self.switch_to_screen(42)
    def menu_metodos(self): self.switch_to_screen(43)
    def menu_principios(self): self.switch_to_screen(44)
    def menu_desperdicios(self): self.switch_to_screen(45)
    def menu_configuracoes(self): self.switch_to_screen(46)
    def menu_relatorios(self): self.switch_to_screen(47)
    
    # Utilitários
    def switch_to_login(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def switch_to_screen(self, index):
        screen = self.stacked_widget.widget(index)
        if hasattr(screen, 'update_user_info'):
            screen.update_user_info()
        self.stacked_widget.setCurrentIndex(index)
    
    def update_user_info(self):
        # Implemente com seus dados reais
        self.perfil.setText("Usuário: Admin")