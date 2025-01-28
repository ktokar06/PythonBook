<h1 align="center">Hi there, I'm<a ></a> Kirill</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center"> Student, Java Developer 🇷🇺 </h3>


# 📜 Phonebook Application

This application is a GUI-based phonebook implemented in Python using the Tkinter library for the user interface and MySQL/MariaDB for backend data storage. The application allows users to manage contacts with features such as viewing, adding, editing, and deleting entries.

## 📦 Installation

1. Clone repositories:
   
 ```bash
 git clone https://github.com/ktokar06/PythonBook.git
 ```

2. Go to the project directory:
   
```bash
cd Phonebook
```
   
3. Start the Database Server: Ensure your MySQL/MariaDB server is running.

4. Run the Application
  
``` python
python app.py
```

5.Use the GUI

  - Navigate between tabs to add, view, edit, or delete contacts.

6.Set Up Database

- Create a database named db_Book in your MySQL/MariaDB server.

- Ensure your database user has appropriate privileges to read, write, and modify data.

```sql
CREATE DATABASE db_Book;
```

7. ``Install Dependencies``
   
  - Install the required Python library:

  ``
  pip install mysql-connector-python
  ``

8. ``Clone or Download the Repository``
   
  Place all files of this project in a single directory.

9. ``Configure Database Parameters``
   
  Update the db_params dictionary in the source code with your database connection details:
  
  ```python
  db_params = {
      'host': 'localhost',
      'port': 3306,
      'user': 'root',
      'password': 'your_password',
      'database': 'db_Book',
      'charset': 'utf8mb4',
  }
  ```

## 💻 Features

- Add Contacts: Add new entries with name, phone number, email, and address.

- View Contacts: Display all stored contacts in a treeview.

- Edit Contacts: Modify existing contact information.

- Delete Contacts: Remove unwanted contacts from the database.

## 🛠️ Technologies Used

- Python: Core language for the application.

- Tkinter: GUI framework.

- MySQL Connector: Interface for connecting to MariaDB/MySQL databases.

- MariaDB/MySQL: Relational database to store contact information.

## 📄 Requirements

- Python 3.7+

- MySQL/MariaDB Database Server

- Python Libraries:

- mysql-connector-python

- tkinter



## Application Structure

### Files

- app.py: Main file that initializes the GUI.

- model.py: Handles interaction with the database.

- db_base.py: Contains database configuration and helper methods.

## Database Schema

The database consists of a single table named contacts:

```sql
CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255),
    address TEXT
);
```



