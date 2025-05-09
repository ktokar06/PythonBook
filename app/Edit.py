from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

class EditContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/edit_contact_dialog.ui', self)
        self.setWindowModality(Qt.ApplicationModal)

        self.saveButton.clicked.connect(self.accept)