import tkinter as tk
from tkinter import ttk, messagebox

class PhonebookApp:

    def __init__(self, model):
        """
        Инициализация приложения.

        :param model: Модель, обеспечивающая логику работы с данными.
        """
        self.model = model
        self.root = tk.Tk()
        self.root.title("Телефонная книга")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TButton",
            background="#6200ea",
            foreground="white",
            padding=10,
            font=("Helvetica", 12, "bold"),
            borderwidth=0,
            relief="flat"
        )
        style.map(
            "TButton",
            background=[("active", "#3700b3")],
            foreground=[("active", "white")]
        )

        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#333333",
            fieldbackground="#ffffff",
            font=("Helvetica", 11),
            rowheight=25,
            bordercolor="#e0e0e0",
            borderwidth=1
        )
        style.configure(
            "Treeview.Heading",
            background="#6200ea",
            foreground="white",
            font=("Helvetica", 12, "bold"),
            padding=10,
            relief="flat"
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#3700b3")]
        )

        style.configure(
            "TScrollbar",
            gripcount=0,
            background="#e0e0e0",
            troughcolor="#f5f5f5",
            bordercolor="#e0e0e0",
            arrowcolor="#6200ea",
            relief="flat"
        )
        style.map(
            "TScrollbar",
            background=[("active", "#3700b3")]
        )

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.contacts_frame = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.contacts_frame, text="Просмотр контактов")

        self.contact_tree = ttk.Treeview(
            self.contacts_frame,
            columns=("ID", "Name", "Phone", "Email", "Address"),
            show="headings",
            style="Treeview"
        )
        self.contact_tree.heading("ID", text="ID", anchor="center")
        self.contact_tree.heading("Name", text="ФИО", anchor="center")
        self.contact_tree.heading("Phone", text="Телефон", anchor="center")
        self.contact_tree.heading("Email", text="Email", anchor="center")
        self.contact_tree.heading("Address", text="Адрес", anchor="center")
        self.contact_tree.column("ID", width=50, anchor="center")
        self.contact_tree.column("Name", width=150, anchor="w")
        self.contact_tree.column("Phone", width=120, anchor="center")
        self.contact_tree.column("Email", width=200, anchor="w")
        self.contact_tree.column("Address", width=300, anchor="w")
        self.contact_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.delete_contact_frame = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.delete_contact_frame, text="Удаление/Редактирование контакта")

        self.delete_contact_list = tk.Listbox(
            self.delete_contact_frame,
            bg="#ffffff",
            fg="#333333",
            font=("Helvetica", 12),
            selectbackground="#6200ea",
            selectforeground="white",
            selectmode=tk.SINGLE,
            relief="flat",
            borderwidth=1
        )
        self.delete_contact_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.delete_contact_scrollbar = ttk.Scrollbar(self.delete_contact_frame, style="TScrollbar")
        self.delete_contact_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.delete_contact_list.config(yscrollcommand=self.delete_contact_scrollbar.set)
        self.delete_contact_scrollbar.config(command=self.delete_contact_list.yview)

        contact_buttons_frame = tk.Frame(self.delete_contact_frame, bg="#ffffff")
        contact_buttons_frame.pack(side=tk.BOTTOM, pady=10)

        edit_button = ttk.Button(contact_buttons_frame, text="Редактировать", command=self.edit_contact)
        edit_button.pack(side=tk.LEFT, padx=10)

        delete_button = ttk.Button(contact_buttons_frame, text="Удалить", command=self.delete_contact)
        delete_button.pack(side=tk.LEFT, padx=10)

        self.add_contact_frame = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.add_contact_frame, text="Добавить контакт")

        self.create_contact_form(self.add_contact_frame)

        self.load_contacts()
        self.root.mainloop()

    def create_contact_form(self, parent):
        """
        Создает форму для добавления нового контакта.

        :param parent: Родительский виджет, в котором будет размещена форма.
        """
        labels = ["ФИО:", "Телефон:", "Email:", "Адрес:"]
        self.entries = {}
        for label in labels:
            label_widget = tk.Label(parent, text=label, bg="#ffffff", font=("Helvetica", 12, "bold"), fg="#333333")
            label_widget.pack(pady=5, anchor="w")

            if label == "Адрес:":
                entry_widget = tk.Text(parent, bg="#ffffff", fg="#333333", font=("Helvetica", 12), height=5, padx=10, pady=5, relief="flat", borderwidth=1)
            else:
                entry_widget = tk.Entry(parent, bg="#ffffff", fg="#333333", font=("Helvetica", 12), relief="flat", borderwidth=1)

            entry_widget.pack(pady=5, fill=tk.X, padx=10)
            self.entries[label] = entry_widget

        add_button = ttk.Button(parent, text="Добавить", command=self.add_contact)
        add_button.pack(pady=20, padx=10)

    def add_contact(self):
        """Добавляет новый контакт в базу данных и обновляет интерфейс."""
        name = self.entries["ФИО:"].get()
        phone = self.entries["Телефон:"].get()
        email = self.entries["Email:"].get()
        address = self.entries["Адрес:"].get("1.0", tk.END).strip()

        if not name or not phone:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните имя и телефон")
            return

        success = self.model.add_contact(name, phone, email, address)
        if success:
            messagebox.showinfo("Успех", "Контакт успешно добавлен")
            self.load_contacts()
            for entry in self.entries.values():
                if isinstance(entry, tk.Text):
                    entry.delete("1.0", tk.END)
                else:
                    entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Контакт с таким телефоном уже существует")

    def delete_contact(self):
        """Удаляет выбранный контакт из базы данных и обновляет интерфейс."""
        selected_item = self.delete_contact_list.curselection()
        if selected_item:
            contact_id = self.delete_contact_list.get(selected_item[0])[0]
            self.model.delete_contact(contact_id)
            self.load_contacts()
        else:
            messagebox.showerror("Ошибка", "Выберите контакт для удаления")

    def edit_contact(self):
        """Открывает диалоговое окно для редактирования выбранного контакта."""
        selected_item = self.delete_contact_list.curselection()
        if selected_item:
            contact_id = self.delete_contact_list.get(selected_item[0])[0]
            contact_details = self.model.get_contact(contact_id)

            if contact_details:
                self.open_edit_dialog(contact_id, contact_details)
            else:
                messagebox.showerror("Ошибка", "Не удалось получить контакт")
        else:
            messagebox.showerror("Ошибка", "Выберите контакт для редактирования")

    def open_edit_dialog(self, contact_id, contact_details):
        """
        Открывает диалоговое окно для редактирования контакта.

        :param contact_id: ID контакта для редактирования.
        :param contact_details: Данные контакта.
        """
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать контакт")
        edit_window.geometry("500x600")
        edit_window.configure(bg="#ffffff")

        labels = ["ФИО:", "Телефон:", "Email:", "Адрес:"]
        self.edit_entries = {}
        for i, (label, detail) in enumerate(zip(labels, contact_details)):
            label_widget = tk.Label(edit_window, text=label, bg="#ffffff", font=("Helvetica", 12, "bold"), fg="#333333")
            label_widget.pack(pady=5, anchor="w")

            if label == "Адрес:":
                entry_widget = tk.Text(edit_window, bg="#ffffff", fg="#333333", font=("Helvetica", 12), height=5, relief="flat", borderwidth=1)
                entry_widget.insert("1.0", detail if detail else "")
            else:
                entry_widget = tk.Entry(edit_window, bg="#ffffff", fg="#333333", font=("Helvetica", 12), relief="flat", borderwidth=1)
                entry_widget.insert(0, detail if detail else "")

            entry_widget.pack(pady=5, fill=tk.X, padx=10)
            self.edit_entries[label] = entry_widget

        save_button = ttk.Button(edit_window, text="Сохранить", command=lambda: self.save_edit(contact_id, edit_window))
        save_button.pack(pady=20, padx=10)

    def save_edit(self, contact_id, edit_window):
        """
        Сохраняет изменения в контакте и закрывает диалоговое окно.

        :param contact_id: ID контакта.
        :param edit_window: Окно редактирования.
        """
        name = self.edit_entries["ФИО:"].get()
        phone = self.edit_entries["Телефон:"].get()
        email = self.edit_entries["Email:"].get()
        address = self.edit_entries["Адрес:"].get("1.0", tk.END).strip()

        if not name or not phone:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните имя и телефон")
            return

        success = self.model.update_contact(contact_id, name, phone, email, address)
        if success:
            messagebox.showinfo("Успех", "Контакт успешно обновлен")
            self.load_contacts()
            edit_window.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить контакт")

    def load_contacts(self):
        """Загружает список контактов из базы данных и отображает их в интерфейсе."""
        self.contact_tree.delete(*self.contact_tree.get_children())
        self.delete_contact_list.delete(0, tk.END)

        contacts = self.model.get_all_contacts()

        for contact in contacts:
            if len(contact) < 5:
                continue

            self.contact_tree.insert("", tk.END, values=contact)
            self.delete_contact_list.insert(tk.END, (contact[0], contact[1]))