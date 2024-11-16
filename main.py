import mysql.connector
from mysql.connector import Error
from db_base import PhonebookModel
from model import PhonebookApp

db_params = {
    'host': 'localhost', 
    'port': 3306,       
    'user': 'root',
    'password': 'secret',
    'database': 'db_Book',
    'charset': 'utf8mb4',  
}

conn = None

try:
    conn = mysql.connector.connect(**db_params)

    if conn.is_connected():
        print("Connected to the database")
except Error as e:
    print(f"Connection failed: {e}")
finally:
    if conn is not None and conn.is_connected():
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    model = PhonebookModel(db_params)
    app = PhonebookApp(model)