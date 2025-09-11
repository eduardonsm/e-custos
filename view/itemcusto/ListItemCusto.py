from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QMessageBox, QTableView,
                               QLineEdit, QComboBox, QAbstractItemView, QHeaderView,QStyle)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt
from model.Session import Session
from model.ItemCustoRepository import ItemCustoRepository

class ListItemCustoWindow(QWidget):
    def __init__(self, stacked_widget, register_item_custo_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        # Guarda uma referência à tela de cadastro para poder chamá-la no modo de edição
        self.register_item_custo_window = register_item_custo_window
        
        self.item_custo_repo = ItemCustoRepository()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Cabeçalho (Padrão) ---
        header_layout = QHBoxLayout()
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        header_layout.addStretch(1)
        home_button = QPushButton("Início")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(29))
        header_layout.addWidget(home_button)
        sair_button = QPushButton("Sair")
        sair_button.clicked.connect(self.logout_and_switch_to_welcome)
        header_layout.addWidget(sair_button)
        self.perfil_label = QLabel()
        header_layout.addWidget(self.perfil_label)
        main_layout.addLayout(header_layout)

        # --- Divisória (Padrão) ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # --- Título ---
        title = QLabel("Itens de Custo Cadastrados")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # --- Controles de Busca e Filtro ---
        controls_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Buscar por Produto ID ou Descrição...")
        self.txt_search.returnPressed.connect(self.load_itens_custo)
        
        self.combo_filter_categoria = QComboBox()
        self.combo_filter_categoria.addItems(["Todas as Categorias", "MD", "MOD", "CIF", "CO"])
        
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.load_itens_custo)
        
        controls_layout.addWidget(self.txt_search)
        controls_layout.addWidget(self.combo_filter_categoria)
        controls_layout.addWidget(btn_buscar)
        main_layout.addLayout(controls_layout)

        # --- Tabela de Itens de Custo ---
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        
        # Configurações da tabela
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        
        main_layout.addWidget(self.table_view)

        # --- Botões de Ação ---
        action_layout = QHBoxLayout()
        action_layout.addStretch() # Alinha os botões à direita

        btn_adicionar = QPushButton("Adicionar Novo")
        btn_adicionar.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        btn_adicionar.clicked.connect(self.adicionar_item)

        btn_editar = QPushButton("Editar Selecionado")
        btn_editar.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        btn_editar.clicked.connect(self.editar_item)

        btn_excluir = QPushButton("Excluir Selecionado")
        btn_excluir.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        btn_excluir.clicked.connect(self.excluir_item)

        action_layout.addWidget(btn_adicionar)
        action_layout.addWidget(btn_editar)
        action_layout.addWidget(btn_excluir)
        main_layout.addLayout(action_layout)

    def load_data(self):
        """Método principal para carregar e recarregar os dados da tela."""
        self.update_user_info()
        self.load_itens_custo()

    def load_itens_custo(self):
        """Busca os itens no banco de dados e popula a tabela."""
        self.model.clear()
        headers = ["ID", "Produto ID", "Descrição", "Qtd", "Medida", "Vlr. Unitário", "Vlr. Total", "Categoria", "Classificação"]
        self.model.setHorizontalHeaderLabels(headers)
        
        user_id = Session().user_id
        if not user_id:
            return

        search_term = self.txt_search.text().strip()
        categoria_filter = self.combo_filter_categoria.currentText()

        try:
            # Lógica de busca e filtro
            if search_term:
                itens = self.item_custo_repo.search_itens(search_term, user_id)
            elif categoria_filter != "Todas as Categorias":
                itens = self.item_custo_repo.get_itens_by_categoria(categoria_filter, user_id)
            else:
                itens = self.item_custo_repo.get_itens_by_user(user_id)

            # Popula o modelo da tabela
            for item in itens:
                row = [
                    QStandardItem(str(item.id)),
                    QStandardItem(item.produto_id),
                    QStandardItem(item.descricao),
                    QStandardItem(f"{item.quantidade:.4f}"),
                    QStandardItem(item.medida),
                    QStandardItem(f"R$ {item.valor_unitario:.4f}"),
                    QStandardItem(f"R$ {item.valor_total:.2f}"),
                    QStandardItem(item.categoria),
                    QStandardItem(item.classificacao)
                ]
                self.model.appendRow(row)

            self.table_view.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Não foi possível carregar os itens de custo:\n{e}")
            
    def adicionar_item(self):
        """Muda para a tela de cadastro em modo de 'novo item'."""
        # Supondo que a tela de cadastro tenha um método para resetar
        self.register_item_custo_window.limpar_formulario() 
        self.register_item_custo_window.update_user_info()
        self.stacked_widget.setCurrentWidget(self.register_item_custo_window)

    def editar_item(self):
        """Pega o ID do item selecionado e abre a tela de cadastro em modo de 'edição'."""
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Atenção", "Selecione um item na tabela para editar.")
            return

        item_id = int(self.model.item(index.row(), 0).text())
        
        # NOTE: Para a edição funcionar, a tela RegisterItemCustoWindow
        # precisará de um método para carregar os dados de um item existente.
        QMessageBox.information(self, "Edição", f"A funcionalidade de edição para o item ID {item_id} deve ser implementada na tela de cadastro.")
        # Exemplo de como seria a chamada:
        # self.register_item_custo_window.load_item_for_edit(item_id)
        # self.stacked_widget.setCurrentWidget(self.register_item_custo_window)

    def excluir_item(self):
        """Exclui o item selecionado do banco de dados após confirmação."""
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Atenção", "Selecione um item na tabela para excluir.")
            return

        item_id = int(self.model.item(index.row(), 0).text())
        produto_id = self.model.item(index.row(), 1).text()
        descricao = self.model.item(index.row(), 2).text()
        
        reply = QMessageBox.question(self, "Confirmar Exclusão", 
                                     f"Tem certeza que deseja excluir o item?\n\nID: {item_id}\nProduto: {produto_id}\nDescrição: {descricao}",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.item_custo_repo.delete_item_custo(item_id, Session().user_id):
                    QMessageBox.information(self, "Sucesso", "Item de custo excluído com sucesso.")
                    self.load_itens_custo() # Recarrega a tabela
                else:
                    QMessageBox.warning(self, "Falha", "Não foi possível excluir o item.")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao excluir o item:\n{e}")

    def logout_and_switch_to_welcome(self):
        self.stacked_widget.setCurrentIndex(0)

    def update_user_info(self):
        session = Session()
        username = session.username if session.username else "Não conectado"
        self.perfil_label.setText(f"Usuário: {username}")