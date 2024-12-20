import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

class RegistrationApp:
    def __init__(self, master):
        self.master = master
        master.title("Авторизация")

        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT
            )
        ''')
        self.conn.commit()

        # Поля для ввода логина и пароля
        tk.Label(master, text="Логин:").grid(row=0, column=0, padx=5, pady=5)
        self.login_entry = tk.Entry(master)
        self.login_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Пароль:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Кнопки
        tk.Button(master, text="Войти", command=self.login).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(master, text="Регистрация", command=self.open_registration_window).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.status_label = tk.Label(master, text="")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.status_label.config(text="Введите логин и пароль.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.cursor.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, hashed_password))
        user = self.cursor.fetchone()

        if user:
            self.status_label.config(text="Успешная авторизация!")
            # Здесь можно вызвать какое-либо другое событие или действие при успешной авторизации
        else:
            self.status_label.config(text="Неверный логин или пароль.")

    def open_registration_window(self):
        self.registration_window = tk.Toplevel(self.master)
        self.registration_window.title("Регистрация")
        RegistrationWindow(self.registration_window, self)

    def close_connection(self):
        self.conn.close()

class RegistrationWindow:
    def __init__(self, master, parent_app):
        self.master = master
        self.parent_app = parent_app

        tk.Label(master, text="Логин:").grid(row=0, column=0, padx=5, pady=5)
        self.reg_login_entry = tk.Entry(master)
        self.reg_login_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Пароль:").grid(row=1, column=0, padx=5, pady=5)
        self.reg_password_entry = tk.Entry(master, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(master, text="Подтвердите пароль:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_confirm_password_entry = tk.Entry(master, show="*")
        self.reg_confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(master, text="Зарегистрироваться", command=self.register_user).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def register_user(self):
        username = self.reg_login_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают.")
            return

        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.parent_app.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            self.parent_app.conn.commit()
            messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован.")
            self.master.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при регистрации: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()
    app.close_connection()