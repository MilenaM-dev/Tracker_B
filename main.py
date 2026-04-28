import tkinter as tk
from tkinter import ttk, messagebox
import json

# Загрузка данных
try:
    with open("books.json", "r", encoding="utf-8") as f:
        books = json.load(f)
except:
    books = []

def save_books():
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def update_table(data=None):
    for row in tree.get_children():
        tree.delete(row)
    
    if data is None:
        data = books
    
    for b in data:
        tree.insert("", tk.END, values=(b["title"], b["author"], b["genre"], b["pages"]))

def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages = pages_entry.get().strip()
    
    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return
    
    try:
        pages = int(pages)
        if pages <= 0:
            messagebox.showerror("Ошибка", "Страниц должно быть больше 0!")
            return
    except:
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
        return
    
    books.append({
        "title": title,
        "author": author,
        "genre": genre,
        "pages": pages
    })
    
    save_books()
    update_table()
    
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)
    
    messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")

def delete_book():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите книгу!")
        return
    
    for item in selected:
        idx = int(item)
        books.pop(idx)
    
    save_books()
    update_table()

def filter_books():
    genre_filter = genre_filter_entry.get().strip().lower()
    pages_filter = pages_filter_entry.get().strip()
    
    filtered = books.copy()
    
    if genre_filter:
        filtered = [b for b in filtered if genre_filter in b["genre"].lower()]
    
    if pages_filter:
        try:
            p = int(pages_filter)
            filtered = [b for b in filtered if b["pages"] > p]
        except:
            messagebox.showerror("Ошибка", "Страницы для фильтра - число!")
            return
    
    update_table(filtered)

def reset_filter():
    genre_filter_entry.delete(0, tk.END)
    pages_filter_entry.delete(0, tk.END)
    update_table()

# Окно
root = tk.Tk()
root.title("Book Tracker")
root.geometry("750x550")

# Заголовок
tk.Label(root, text="МОЯ БИБЛИОТЕКА", font=("Arial", 16, "bold")).pack(pady=10)

# Рамка для добавления
add_frame = tk.Frame(root, relief="groove", bd=2)
add_frame.pack(fill="x", padx=10, pady=5)

tk.Label(add_frame, text="ДОБАВИТЬ КНИГУ", font=("Arial", 10, "bold")).pack(pady=5)

row1 = tk.Frame(add_frame)
row1.pack(pady=5)

tk.Label(row1, text="Название:").grid(row=0, column=0, padx=5)
title_entry = tk.Entry(row1, width=20)
title_entry.grid(row=0, column=1, padx=5)

tk.Label(row1, text="Автор:").grid(row=0, column=2, padx=5)
author_entry = tk.Entry(row1, width=15)
author_entry.grid(row=0, column=3, padx=5)

row2 = tk.Frame(add_frame)
row2.pack(pady=5)

tk.Label(row2, text="Жанр:").grid(row=0, column=0, padx=5)
genre_entry = tk.Entry(row2, width=15)
genre_entry.grid(row=0, column=1, padx=5)

tk.Label(row2, text="Страниц:").grid(row=0, column=2, padx=5)
pages_entry = tk.Entry(row2, width=10)
pages_entry.grid(row=0, column=3, padx=5)

tk.Button(add_frame, text="ДОБАВИТЬ КНИГУ", command=add_book, bg="green", fg="white").pack(pady=5)

# Рамка для фильтров
filter_frame = tk.Frame(root, relief="groove", bd=2)
filter_frame.pack(fill="x", padx=10, pady=5)

tk.Label(filter_frame, text="ФИЛЬТРАЦИЯ", font=("Arial", 10, "bold")).pack(pady=5)

row_f = tk.Frame(filter_frame)
row_f.pack(pady=5)

tk.Label(row_f, text="Жанр:").grid(row=0, column=0, padx=5)
genre_filter_entry = tk.Entry(row_f, width=15)
genre_filter_entry.grid(row=0, column=1, padx=5)

tk.Label(row_f, text="Страниц >").grid(row=0, column=2, padx=5)
pages_filter_entry = tk.Entry(row_f, width=8)
pages_filter_entry.grid(row=0, column=3, padx=5)

tk.Button(row_f, text="ФИЛЬТР", command=filter_books, bg="blue", fg="white").grid(row=0, column=4, padx=5)
tk.Button(row_f, text="СБРОС", command=reset_filter, bg="orange").grid(row=0, column=5, padx=5)

# Таблица
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("Название", "Автор", "Жанр", "Страниц")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

tree.heading("Название", text="Название")
tree.heading("Автор", text="Автор")
tree.heading("Жанр", text="Жанр")
tree.heading("Страниц", text="Страниц")

tree.column("Название", width=200)
tree.column("Автор", width=120)
tree.column("Жанр", width=100)
tree.column("Страниц", width=80)

scroll = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)

tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# Кнопка удаления
tk.Button(root, text="УДАЛИТЬ ВЫБРАННУЮ КНИГУ", command=delete_book, bg="red", fg="white").pack(pady=10)

update_table()
root.mainloop()