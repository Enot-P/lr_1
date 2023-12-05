import tkinter as tk
from tkinter import ttk, filedialog
from fitz import fitz


class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Библиотечная Система")
        self.root.geometry("800x600")

        # Фиктивная база данных книг
        self.books = {
            "Грокаем алгоритмы": "/home/enot/Downloads/aditya bhargava grok.pdf",
            "PRO GIT": "/home/enot/Downloads/progit.pdf",
            # Добавьте свои книги и соответствующие PDF-файлы
        }

        # Вход в систему
        self.login_frame = ttk.Frame(self.root, padding="10")
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.show_login()

    def show_login(self):
        ttk.Label(self.login_frame, text="Введите логин и пароль").grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.login_frame, text="Логин:").grid(row=1, column=0, sticky="e")
        ttk.Entry(self.login_frame, show="*").grid(row=1, column=1)
        ttk.Label(self.login_frame, text="Пароль:").grid(row=2, column=0, sticky="e")
        ttk.Entry(self.login_frame, show="*").grid(row=2, column=1)
        ttk.Button(self.login_frame, text="Войти", command=self.show_library).grid(row=3, column=0, columnspan=2,
                                                                                   pady=10)

    def show_library(self):
        # Очистка предыдущего окна
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.login_frame, text="Выберите книгу:").grid(row=0, column=0, columnspan=2, pady=10)

        # Создание списка книг
        book_listbox = tk.Listbox(self.login_frame)
        for book in self.books:
            book_listbox.insert(tk.END, book)
        book_listbox.grid(row=1, column=0, columnspan=2)

        # Кнопка для открытия PDF
        ttk.Button(self.login_frame, text="Открыть PDF", command=lambda: self.open_pdf(book_listbox)).grid(row=2,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=10)

    def open_pdf(self, book_listbox):
        selected_book = book_listbox.get(book_listbox.curselection())
        pdf_path = self.books.get(selected_book)

        if pdf_path:
            pdf_window = tk.Toplevel(self.root)
            pdf_window.title(selected_book)

            pdf_canvas = tk.Canvas(pdf_window)
            pdf_canvas.pack(fill=tk.BOTH, expand=tk.YES)

            scrollbar = ttk.Scrollbar(pdf_window, orient=tk.VERTICAL, command=pdf_canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            pdf_canvas.configure(yscrollcommand=scrollbar.set)

            pdf_document = fitz.open(pdf_path)

            for page_number in range(pdf_document.page_count()):
                page = pdf_document[page_number]
                img = page.get_pixmap()
                img_width = img.width
                img_height = img.height

                pdf_canvas.config(scrollregion=pdf_canvas.bbox("all"))
                pdf_canvas.create_image(0, 0, anchor=tk.NW, image=tk.PhotoImage(data=img.tobytes("ppm"), width=img_width, height=img_height))

        else:
            tk.messagebox.showerror("Ошибка", "Выберите книгу для открытия PDF")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()
