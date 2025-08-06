from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                               QLabel, QPushButton, QHBoxLayout, QFrame, QScrollArea, QMessageBox,QDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from model.Session import Session
from model.ProductRepository import ProductRepository
from viewModel.ProductController import ProductController
from view.product.UpdateProjectDialog import UpdateProductDialog

class ListCostWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Layout principal que conterá o cabeçalho e a área de rolagem
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # --- Cabeçalho (reutilizado de outras telas) ---
        header_layout = QHBoxLayout()
        
        icon = QLabel()
        pixmap = QPixmap("./images/ecustos-logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        header_layout.addWidget(icon)
        
        header_layout.addStretch(1)

        sair_button = QPushButton("Sair")
        sair_button.setObjectName("sair")
        sair_button.clicked.connect(self.logout_and_switch_to_welcome)
        voltar_button = QPushButton("Voltar")
        voltar_button.setObjectName("Voltar")
        voltar_button.clicked.connect(self.back_to_home)
        header_layout.addWidget(voltar_button)
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

        # --- Título ---
        self.title = QLabel("Produtos Cadastrados")
        self.title.setObjectName("pergunta") # Usando o mesmo estilo do formulário
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        # --- Área de Rolagem para o conteúdo principal ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Essencial para o layout interno se ajustar
        scroll_area.setFrameShape(QFrame.NoFrame) # Remove a borda da área de rolagem
        main_layout.addWidget(scroll_area)

        # --- Widget de Conteúdo (que ficará dentro da área de rolagem) ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget) # Layout para o conteúdo
        content_layout.setSpacing(15)

        # Tabela de produtos adicionada ao layout do conteúdo
        self.table = QTableWidget()
        content_layout.addWidget(self.table)

        # Layout para centralizar o botão de atualizar
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.load_products)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch(1)
        content_layout.addLayout(button_layout)

        # Define o widget de conteúdo como o widget da área de rolagem
        scroll_area.setWidget(content_widget)


    def load_products(self):
        user_id = Session().user_id
        if user_id is None:
            self.title.setText("Usuário não está logado.")
            self.table.setRowCount(0) # Limpa a tabela se não houver usuário
            return

        repo = ProductRepository()
        products = repo.get_products_by_user(user_id)
        
        self.title.setText(f"Produtos Cadastrados ({len(products)})")

        self.table.setRowCount(len(products))
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Nome", "Data Projeto", "Data Início", "Ativo", "Data Fim", "Preço", "Árvore do Produto", "Editar", "Excluir"
        ])

        for row_idx, product in enumerate(products):
            self.table.setItem(row_idx, 0, QTableWidgetItem(product.name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(product.dateProject)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(product.dateStart)))
            self.table.setItem(row_idx, 3, QTableWidgetItem("Sim" if product.isActive else "Não"))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(product.endTime) if product.endTime else "N/A"))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"R$ {product.price:.2f}"))
            self.table.setItem(row_idx, 6, QTableWidgetItem(product.productTree))
            # Botão de Editar
            update_button = QPushButton("Editar")
            update_button.clicked.connect(lambda checked, pid=product.id: self.updateProduct(pid))
            self.table.setCellWidget(row_idx, 7, update_button)

            # Botão de Excluir
            delete_button = QPushButton("Excluir")
            delete_button.clicked.connect(lambda checked, pid=product.id: self.deleteProduct(pid))
            self.table.setCellWidget(row_idx, 8, delete_button)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    # --- utils ---
    def updateProduct(self, product_id):
        user_id = Session().user_id
        if not user_id:
            return
        confirm_reply = QMessageBox.question(self, 'Confirmar Edição',
                                         f"Tem certeza que deseja editar o produto {product_id}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm_reply == QMessageBox.Yes:
            pController = ProductController()
            try:
                productToUpdate = pController.get_product_by_id(product_id, user_id=user_id)

                dialog = UpdateProductDialog(productToUpdate, self)
                if dialog.exec() == QDialog.Accepted:
                    updated_product = dialog.get_updated_data()
                    if updated_product:
                        pController.update_product(product_id=product_id, user_id=user_id, name=updated_product.name,
                                                   dateProject=updated_product.dateProject,
                                                   dateStart=updated_product.dateStart,
                                                   isActive=updated_product.isActive,
                                                   endTime=updated_product.endTime,
                                                   price=updated_product.price,
                                                   productTree=updated_product.productTree)
                        QMessageBox.information(self, "Sucesso", "Produto atualizado com sucesso.")
                        self.load_products()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível atualizar o produto: {e}")
    def deleteProduct(self, product_id):
        userId = Session().user_id
        if not userId:
            return

        confirm_reply = QMessageBox.question(self, 'Confirmar Exclusão', 
                                         f"Tem certeza que deseja excluir o produto {product_id}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm_reply == QMessageBox.Yes:
            pController = ProductController()
            try:
                pController.delete_product(product_id, user_id=userId)
                QMessageBox.information(self, "Sucesso", "Produto excluído com sucesso.")
                self.load_products() 
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível excluir o produto: {e}")

    def update_user_info(self):
        session = Session()
        username_display = session.username if session.username else "Não Conectado"
        self.perfil_label.setText(f"Conectado: {username_display}")
    def logout_and_switch_to_welcome(self):
        Session.user_id = None
        Session.username = None
        self.stacked_widget.setCurrentIndex(0)
    def back_to_home(self):
        self.stacked_widget.setCurrentIndex(29)