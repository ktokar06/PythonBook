from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QDialog, QAbstractItemView, QTableWidgetItem)

from Edit import EditContactDialog

class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        uic.loadUi('../ui/main_window.ui', self)

        self.model = model
        self.sorted_asc = False

        self.init_ui()
        self.load_contacts()

    def init_ui(self):
        self.contactsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contactsTable.setSelectionMode(QAbstractItemView.SingleSelection)

        self.searchEdit.textChanged.connect(self.handle_search)
        self.sortButton.clicked.connect(self.toggle_sort)

        self.addButton.clicked.connect(self.add_contact)
        self.editButton.clicked.connect(self.edit_contact)
        self.deleteButton.clicked.connect(self.delete_contact)

        self.searchEdit.setPlaceholderText("Введите имя, телефон или адрес...")

    def load_contacts(self):
        search_query = self.searchEdit.text().lower()
        if search_query == "введите имя, телефон или адрес...":
            search_query = ""

        contacts = self.model.get_all_contacts()

        if search_query:
            contacts = [
                c for c in contacts
                if (search_query in c[1].lower() or
                    search_query in c[2].lower() or
                    (c[3] and search_query in c[3].lower()) or
                    (c[4] and search_query in c[4].lower()))
            ]

        contacts = sorted(contacts, key=lambda x: x[1].lower(), reverse=self.sorted_asc)

        self.contactsTable.setRowCount(0)
        self.contactsTable.setColumnCount(5)
        self.contactsTable.setHorizontalHeaderLabels(['ID', 'ФИО', 'Телефон', 'Email', 'Адрес'])

        self.contactsList.clear()

        for contact in contacts:
            if len(contact) < 5:
                continue

            row = self.contactsTable.rowCount()
            self.contactsTable.insertRow(row)
            for col, value in enumerate(contact):
                self.contactsTable.setItem(row, col, QTableWidgetItem(str(value)))

            self.contactsList.addItem(f"{contact[0]}: {contact[1]}")

    def handle_search(self, text):
        self.load_contacts()

    def toggle_sort(self):
        self.sorted_asc = not self.sorted_asc
        self.sortButton.setText("Сортировать Я-А" if self.sorted_asc else "Сортировать А-Я")
        self.load_contacts()

    def add_contact(self):

        name = self.nameEdit.text().strip()
        phone = self.phoneEdit.text().strip()
        email = self.emailEdit.text().strip()
        address = self.addressEdit.toPlainText().strip()

        if not name or not phone:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, заполните имя и телефон")
            return

        success = self.model.add_contact(name, phone, email, address)
        if success:
            QMessageBox.information(self, "Успех", "Контакт успешно добавлен")
            self.nameEdit.clear()
            self.phoneEdit.clear()
            self.emailEdit.clear()
            self.addressEdit.clear()
            self.load_contacts()
        else:
            QMessageBox.critical(self, "Ошибка", "Контакт с таким телефоном уже существует")

    def delete_contact(self):
        selected_items = self.contactsList.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, "Ошибка", "Выберите контакт для удаления")
            return

        contact_id = selected_items[0].text().split(":")[0]
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить этот контакт?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = self.model.delete_contact(contact_id)
            if success:
                QMessageBox.information(self, "Успех", "Контакт успешно удален")
                self.load_contacts()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось удалить контакт")

    def edit_contact(self):
        selected_items = self.contactsList.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, "Ошибка", "Выберите контакт для редактирования")
            return

        contact_id = selected_items[0].text().split(":")[0]
        contact_details = self.model.get_contact(contact_id)

        if not contact_details:
            QMessageBox.critical(self, "Ошибка", "Не удалось получить контакт")
            return

        dialog = EditContactDialog(self)
        dialog.nameEdit.setText(contact_details[0])
        dialog.phoneEdit.setText(contact_details[1])
        dialog.emailEdit.setText(contact_details[2] if contact_details[2] else "")
        dialog.addressEdit.setPlainText(contact_details[3] if contact_details[3] else "")

        if dialog.exec_() == QDialog.Accepted:
            name = dialog.nameEdit.text().strip()
            phone = dialog.phoneEdit.text().strip()
            email = dialog.emailEdit.text().strip()
            address = dialog.addressEdit.toPlainText().strip()

            if not name or not phone:
                QMessageBox.critical(self, "Ошибка", "Пожалуйста, заполните имя и телефон")
                return

            success = self.model.update_contact(contact_id, name, phone, email, address)
            if success:
                QMessageBox.information(self, "Успех", "Контакт успешно обновлен")
                self.load_contacts()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось обновить контакт")