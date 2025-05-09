# 📜 Телефонная книга (PyQt5 + MySQL)
## 🌟 Обзор

Современное GUI-приложение "Телефонная книга" на PyQt5 с использованием MySQL/MariaDB. Позволяет удобно управлять контактами с полным набором CRUD-операций.

## 📦 Установка

### Требования
- Python 3.7+
- Сервер MySQL/MariaDB
- Git

### Настройка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ktokar06/PythonBook.git
cd PythonBook
```

2. Создайте и активируйте виртуальное окружение (рекомендуется):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3Настройте подключение к БД в `app.py`:
```python
db_params = {
    'host': 'localhost',
    'port': 3306,
    'user': 'ваш_логин',
    'password': 'ваш_пароль',
    'database': 'db_Book',
    'charset': 'utf8mb4',
}
```

## 🚀 Использование

Запустите приложение:
```bash
python app.py
```

### Вкладки приложения:
1. **Просмотр контактов**: Просмотр всех контактов с поиском и сортировкой
2. **Добавление контакта**: Добавление новых контактов со всеми данными
3. **Редактирование/Удаление**: Изменение или удаление существующих контактов

## 📊 Схема базы данных

```sql
CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255),
    address TEXT
);
```
