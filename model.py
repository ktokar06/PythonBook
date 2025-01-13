import tkinter as tk
from tkinter import ttk, messagebox

class PhonebookApp:
    def __init__(self, model):
        self.model = model
        self.root = tk.Tk()
        self.root.title("Телефонная книга")
        self.root.geometry("800x600")
        self.root.configure(bg="#e9eff1")  

        style = ttk.Style()
        style.configure(
            "TButton",
            background="#4a90e2",
            foreground="white",
            padding=10,
            font=("Helvetica", 12),
            relief="flat" 
        )
        style.map(
            "TButton",
            background=[("active", "#357abd")],
            foreground=[("active", "white")]
        )

        style.configure(
            "Treeview",
            background="#f5f5f5",  
            foreground="#333333",  
            fieldbackground="#f5f5f5", 
            font=("Helvetica", 11)
        )
        style.configure(
            "Treeview.Heading",
            background="#4a90e2",
            foreground="white",
            font=("Helvetica", 12, 'bold')
        )

        style.configure(
            "TScrollbar",
            gripcount=0,
            background="#4a90e2",
            troughcolor="#e9eff1",
            borderwidth=0,
            arrowcolor="white"
        )

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)


        self.contacts_frame = tk.Frame(self.notebook, bg="#e9eff1")
        self.notebook.add(self.contacts_frame, text="Просмотр контактов")

        self.contact_tree = ttk.Treeview(
            self.contacts_frame,
            columns=("ID", "Name", "Phone", "Email", "Address"),
            show="headings",
            style="Treeview"
        )
        self.contact_tree.heading("ID", text="ID")
        self.contact_tree.heading("Name", text="Имя")
        self.contact_tree.heading("Phone", text="Телефон")
        self.contact_tree.heading("Email", text="Email")
        self.contact_tree.heading("Address", text="Адрес")
        self.contact_tree.column("ID", width=50, anchor='center')
        self.contact_tree.column("Name", width=150)
        self.contact_tree.column("Phone", width=100)
        self.contact_tree.column("Email", width=150)
        self.contact_tree.column("Address", width=250)
        self.contact_tree.pack(fill=tk.BOTH, expand=True)

        self.delete_contact_frame = tk.Frame(self.notebook, bg="#e9eff1")
        self.notebook.add(self.delete_contact_frame, text="Удаление/Редактирование контакта")

        self.delete_contact_list = tk.Listbox(
            self.delete_contact_frame,
            bg="white",
            fg="black",
            font=("Helvetica", 12),
            selectbackground="#4a90e2",
            selectmode=tk.SINGLE,
            relief="flat"
        )
        self.delete_contact_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.delete_contact_scrollbar = ttk.Scrollbar(self.delete_contact_frame, style="TScrollbar")
        self.delete_contact_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.delete_contact_list.config(yscrollcommand=self.delete_contact_scrollbar.set)
        self.delete_contact_scrollbar.config(command=self.delete_contact_list.yview)

        contact_buttons_frame = tk.Frame(self.delete_contact_frame, bg="#e9eff1")
        contact_buttons_frame.pack(side=tk.BOTTOM, pady=10)

        edit_button = ttk.Button(contact_buttons_frame, text="Редактировать", command=self.edit_contact)
        edit_button.pack(side=tk.LEFT, padx=10)

        delete_button = ttk.Button(contact_buttons_frame, text="Удалить", command=self.delete_contact)
        delete_button.pack(side=tk.LEFT, padx=10)

        self.add_contact_frame = tk.Frame(self.notebook, bg="#e9eff1")
        self.notebook.add(self.add_contact_frame, text="Добавить контакт")

        self.create_contact_form(self.add_contact_frame)

        self.load_contacts()
        self.root.mainloop()

    def create_contact_form(self, parent):
        """Создание формы для добавления контакта."""
        labels = ["Имя:", "Телефон:", "Email:", "Адрес:"]
        self.entries = {}
        for label in labels:
            label_widget = tk.Label(parent, text=label, bg="#e9eff1", font=("Helvetica", 12, 'bold'))
            label_widget.pack(pady=5, anchor='w')

            if label == "Адрес:":
                entry_widget = tk.Text(parent, bg="#ffffff", fg="#000000", font=("Helvetica", 12), height=5, padx=10,
                                    pady=5)
            else:
                entry_widget = tk.Entry(parent, bg="#ffffff", fg="#000000", font=("Helvetica", 12))

            entry_widget.pack(pady=5, fill=tk.X)
            self.entries[label] = entry_widget

        add_button = ttk.Button(parent, text="Добавить", command=self.add_contact)
        add_button.pack(pady=10)

    def create_contact_form(self, parent):
        """Создание формы для добавления контакта."""
        labels = ["Имя:", "Телефон:", "Email:", "Адрес:"]
        self.entries = {}
        for label in labels:
            label_widget = tk.Label(parent, text=label, bg="#f0f8ff", font=("Helvetica", 12, 'bold'))
            label_widget.pack(pady=5, anchor='w')

            if label == "Адрес:":
                entry_widget = tk.Text(parent, bg="white", fg="black", font=("Helvetica", 12), height=5)
            else:
                entry_widget = tk.Entry(parent, bg="white", fg="black", font=("Helvetica", 12))

            entry_widget.pack(pady=5, fill=tk.X)
            self.entries[label] = entry_widget

        add_button = ttk.Button(parent, text="Добавить", command=self.add_contact)
        add_button.pack(pady=10)

    def add_contact(self):
        """Добавление нового контакта в интерфейсе."""
        name = self.entries["Имя:"].get()
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
        """Удаление выбранного контакта в интерфейсе."""
        selected_item = self.delete_contact_list.curselection()
        if selected_item:
            contact_id = self.delete_contact_list.get(selected_item[0])[0]
            self.model.delete_contact(contact_id)
            self.load_contacts()
        else:
            messagebox.showerror("Ошибка", "Выберите контакт для удаления")

    def edit_contact(self):
        """Редактирование выбранного контакта."""
        selected_item = self.delete_contact_list.curselection()
        if selected_item:
            contact_id = self.delete_contact_list.get(selected_item[0])[0]
            print(f"Selected contact ID: {contact_id}")
            contact_details = self.model.get_contact(contact_id)

            if contact_details:
                print(f"Contact details: {contact_details}") 
                self.open_edit_dialog(contact_id, contact_details)
            else:
                messagebox.showerror("Ошибка", "Не удалось получить контакт")
        else:
            messagebox.showerror("Ошибка", "Выберите контакт для редактирования")

    def open_edit_dialog(self, contact_id, contact_details):
        """Открытие диалогового окна для редактирования контакта."""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать контакт")
        edit_window.geometry("500x600")
        edit_window.configure(bg="#f0f8ff")

        labels = ["Имя:", "Телефон:", "Email:", "Адрес:"]
        self.edit_entries = {}  # Initialize or reset the dictionary
        for i, (label, detail) in enumerate(zip(labels, contact_details)):
            label_widget = tk.Label(edit_window, text=label, bg="#f0f8ff", font=("Helvetica", 12, 'bold'))
            label_widget.pack(pady=5, anchor='w')

            if label == "Адрес:":
                entry_widget = tk.Text(edit_window, bg="white", fg="black", font=("Helvetica", 12), height=5)
                entry_widget.insert("1.0", detail if detail else "")  
            else:
                entry_widget = tk.Entry(edit_window, bg="white", fg="black", font=("Helvetica", 12))
                entry_widget.insert(0, detail if detail else "")

            entry_widget.pack(pady=5, fill=tk.X)
            self.edit_entries[label] = entry_widget

        # Debug print to check keys in self.edit_entries
        print("Keys in edit_entries:", self.edit_entries.keys())

        save_button = ttk.Button(edit_window, text="Сохранить", command=lambda: self.save_edit(contact_id, edit_window))
        save_button.pack(pady=10)

    def save_edit(self, contact_id, edit_window):
        """Сохранение изменений редактированного контакта."""
        print("Available keys in edit_entries:", self.edit_entries.keys())

        # Retrieve address safely
        address_entry = self.edit_entries.get("Адрес:")
        if address_entry:
            address = address_entry.get("1.0", tk.END).strip()
        else:
            print("Address entry not found!")
            address = "" 

        name = self.edit_entries.get("Имя:", tk.Entry()).get()
        phone = self.edit_entries.get("Телефон:", tk.Entry()).get()
        email = self.edit_entries.get("Email:", tk.Entry()).get()

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
        """Загрузка списка контактов в интерфейс."""
        self.contact_tree.delete(*self.contact_tree.get_children())
        self.delete_contact_list.delete(0, tk.END)

        contacts = self.model.get_all_contacts()

        for contact in contacts:
            print(f"Contact data: {contact}")  
            if len(contact) < 5:
                print(f"Error: Contact tuple has fewer than 5 elements: {contact}")
                continue  

            self.contact_tree.insert("", tk.END, values=contact)
            self.delete_contact_list.insert(tk.END, (contact[0], contact[1]))

