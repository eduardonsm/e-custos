from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize

class CustomRadioButton(QWidget):
    def __init__(self, text, image_path, group: QButtonGroup,id: int, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # RadioButton (apenas icone)
        self.radio = QRadioButton()
        group.addButton(self.radio, id)
        icon = QIcon(image_path)
        self.radio.setIcon(icon)
        self.radio.setMinimumSize(80, 80)
        self.radio.setIconSize(QSize(50, 50))
        # self.radio.setAutoExclusive(False)  # Se quiser desmarcar manualmente depois
        
        # texto (em baixo)
        image_label = QLabel(text)
        image_label.setObjectName("textButton")
        image_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.radio)
        layout.addWidget(image_label)
        layout.setSpacing(6)
        self.setLayout(layout)

    def isChecked(self):
        return self.radio.isChecked()

    def setChecked(self, value):
        self.radio.setChecked(value)

    def setAutoExclusive(self, value):
        self.radio.setAutoExclusive(value)