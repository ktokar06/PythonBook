import sys
from PyQt5.QtWidgets import QApplication
from app.db_base import PhonebookModel
from app.Home import MainWindow

class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.db_params = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'secret',
            'database': 'db_Book',
            'charset': 'utf8mb4',
        }

        try:
            self.model = PhonebookModel(self.db_params)
            self.main_window = MainWindow(self.model)
            self.main_window.show()
        except Exception as e:
            print(f"Ошибка: {e}")
            sys.exit(1)

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())