import mysql.connector

class PhonebookModel:
    def __init__(self, db_params):
        self.conn, self.cursor = self.connect_db(db_params)
        self.create_tables()

    def connect_db(self, db_params):
        """Подключение к базе данных MariaDB."""
        conn = mysql.connector.connect(**db_params)
        cursor = conn.cursor()
        return conn, cursor

    def create_tables(self):
        self.cursor.execute("SHOW TABLES LIKE 'contacts'")
        result = self.cursor.fetchone()
        if not result:
            self.cursor.execute('''
            CREATE TABLE contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL UNIQUE,
                email VARCHAR(255),
                address TEXT
            )
            ''')

    def add_contact(self, name, phone, email, address):
        """Добавление нового контакта."""
        self.cursor.execute("SELECT id FROM contacts WHERE phone=%s", (phone,))
        if self.cursor.fetchone():
            return False

        self.cursor.execute(
            "INSERT INTO contacts (name, phone, email, address) VALUES (%s, %s, %s, %s)",
            (name, phone, email, address)
        )
        self.conn.commit()
        return True

    def delete_contact(self, contact_id):
        """Удаление контакта по ID."""
        self.cursor.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
        self.conn.commit()

    def get_all_contacts(self):
        """Получение всех контактов из базы данных."""
        query = "SELECT id, name, phone, email, address FROM contacts"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_contact(self, contact_id):
        """Получение данных контакта по ID."""
        self.cursor.execute(
            "SELECT name, phone, email, address FROM contacts WHERE id=%s",
            (contact_id,)
        )
        return self.cursor.fetchone()

    def update_contact(self, contact_id, name, phone, email, address):
        """Обновление данных контакта по ID."""
        self.cursor.execute(
            "UPDATE contacts SET name=%s, phone=%s, email=%s, address=%s WHERE id=%s",
            (name, phone, email, address, contact_id)
        )
        self.conn.commit()
        return True



