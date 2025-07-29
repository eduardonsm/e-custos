import json
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                               QCheckBox, QDialogButtonBox, QTextEdit, QMessageBox)
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDateEdit, QDoubleSpinBox # Adicionado
from model.Product import Product

class UpdateProductDialog(QDialog):
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Produto")
        self.product = product # Armazena o produto original

        # --- Layouts ---
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # --- Widgets do Formulário ---
        self.name_edit = QLineEdit()
        self.date_project_edit = QDateEdit()
        self.date_project_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_start_edit = QDateEdit()
        self.date_start_edit.setDisplayFormat("yyyy-MM-dd")
        self.is_active_check = QCheckBox("Produto Ativo")
        self.end_time_edit = QDateEdit()
        self.end_time_edit.setDisplayFormat("yyyy-MM-dd")
        self.price_edit = QDoubleSpinBox()
        self.price_edit.setRange(0, 9999999.99)
        self.price_edit.setDecimals(2)
        self.price_edit.setPrefix("R$ ")
        self.product_tree_edit = QTextEdit() # Melhor para textos longos como JSON

        # --- Adicionando widgets ao layout do formulário ---
        form_layout.addRow("Nome:", self.name_edit)
        form_layout.addRow("Data do Projeto:", self.date_project_edit)
        form_layout.addRow("Data de Início:", self.date_start_edit)
        form_layout.addRow(self.is_active_check)
        form_layout.addRow("Data de Fim:", self.end_time_edit)
        form_layout.addRow("Preço:", self.price_edit)
        form_layout.addRow("Árvore do Produto (JSON):", self.product_tree_edit)

        layout.addLayout(form_layout)

        # --- Botões de Salvar e Cancelar ---
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # --- Preenche o formulário com os dados atuais do produto ---
        self.populate_form()

    def populate_form(self):
        """Preenche os campos do formulário com os dados do produto."""
        self.name_edit.setText(self.product.name)
        # Converte a data string para QDate
        self.date_project_edit.setDate(QDate.fromString(str(self.product.dateProject), "yyyy-MM-dd"))
        self.date_start_edit.setDate(QDate.fromString(str(self.product.dateStart), "yyyy-MM-dd"))
        self.is_active_check.setChecked(self.product.isActive)
        if self.product.endTime:
            self.end_time_edit.setDate(QDate.fromString(str(self.product.endTime), "yyyy-MM-dd"))
        self.price_edit.setValue(self.product.price)
        self.product_tree_edit.setText(self.product.productTree)

    def get_updated_data(self):
        """Retorna um novo objeto Product com os dados atualizados do formulário."""
        # Validação do JSON
        try:
            json.loads(self.product_tree_edit.toPlainText())
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Erro de Validação", "O texto em 'Árvore do Produto' não é um JSON válido.")
            return None

        return Product(
            name=self.name_edit.text(),
            dateProject=self.date_project_edit.date().toString("yyyy-MM-dd"),
            dateStart=self.date_start_edit.date().toString("yyyy-MM-dd"),
            isActive=self.is_active_check.isChecked(),
            endTime=self.end_time_edit.date().toString("yyyy-MM-dd"),
            price=self.price_edit.value(),
            productTree=self.product_tree_edit.toPlainText(),
            id=self.product.id # Mantém o ID original!
        )