import mysql.connector
from mysql.connector import Error

class PhonebookModel:
    def __init__(self, db_params):
        self.conn, self.cursor = self._connect(db_params)
        self._ensure_table_exists()

    def _connect(self, params):
        try:
            conn = mysql.connector.connect(**params)
            return conn, conn.cursor()
        except Error as e:
            raise RuntimeError(f"Ошибка подключения: {e}")

    def _ensure_table_exists(self):
        """Создает таблицу контактов если она не существует."""
        self.cursor.execute("SHOW TABLES LIKE 'contacts'")
        if not self.cursor.fetchone():
            self.cursor.execute("""
                CREATE TABLE contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(20) NOT NULL UNIQUE,
                    email VARCHAR(255),
                    address TEXT
                )
            """)
            self.conn.commit()

    def add_contact(self, name, phone, email, address):
        try:
            self.cursor.execute("SELECT id FROM contacts WHERE phone=%s", (phone,))
            if self.cursor.fetchone():
                return False

            self.cursor.execute(
                "INSERT INTO contacts (name, phone, email, address) VALUES (%s, %s, %s, %s)",
                (name, phone, email, address)
            )
            self.conn.commit()
            return True
        except Error as e:
            print(f"Ошибка добавления: {e}")
            return False

    def delete_contact(self, contact_id):
        try:
            self.cursor.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
            self.conn.commit()
            return True
        except Error as e:
            print(f"Ошибка удаления: {e}")
            return False

    def get_all_contacts(self):
        try:
            self.cursor.execute("SELECT id, name, phone, email, address FROM contacts")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Ошибка получения данных: {e}")
            return []

    def get_contact(self, contact_id):
        try:
            self.cursor.execute(
                "SELECT name, phone, email, address FROM contacts WHERE id=%s",
                (contact_id,)
            )
            return self.cursor.fetchone()
        except Error as e:
            print(f"Ошибка получения контакта: {e}")
            return None

    def update_contact(self, contact_id, name, phone, email, address):
        try:
            self.cursor.execute(
                "UPDATE contacts SET name=%s, phone=%s, email=%s, address=%s WHERE id=%s",
                (name, phone, email, address, contact_id)
            )
            self.conn.commit()
            return True
        except Error as e:
            print(f"Ошибка обновления: {e}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()