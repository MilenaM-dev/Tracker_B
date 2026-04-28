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
    # Очищаем таблицу
    for row in tree.get_children():
        tree.delete(row)
    
    if data is None:
        data = books
    
    if not data:
        tk.Label(table_frame, text="Список пуст", font=("Arial", 10)).place(x=10, y=10)
        return
    
    for b in data:
        tree.insert("", tk.END, values=(b["title"], b["author"], b["genre"], b["pages"]))

def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages = pages_entry.get().strip()
    
    # Проверка полей
    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return
    
    # Проверка страниц
    try:
        pages = int(pages)
        if pages <= 0:
            messagebox.showerror("Ошибка", "Страниц должно быть больше 0!")
            return
    except:
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
        return
    
    # Добавляем книгу
    books.append({
        "title": title,
        "author": author,
        "genre": genre,
        "pages": pages
    })
    
    save_books()
    update_table()
    
    # Очищаем поля
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)
    
    messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")

def delete_book():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите книгу для удаления!")
        return
    
    # Получаем название выбранной книги
    item = tree.item(selected[0])
    title = item["values"][0]
    
    # Ищем и удаляем по названию
    for i, book in enumerate(books):
        if book["title"] == title:
            books.pop(i)
            break
    
    save_books()
    update_table()
    messagebox.showinfo("Успех", f"Книга '{title}' удалена!")

def filter_books():
    genre_filter = genre_filter_entry.get().strip().lower()
    pages_filter = pages_filter_entry.get().strip()
    
    filtered = books.copy()
    
    # Фильтр по жанру
    if genre_filter:
        filtered = [b for b in filtered if genre_filter in b["genre"].lower()]
    
    # Фильтр по страницам (> значение)
    if pages_filter:
        try:
            p = int(pages_filter)
            filtered = [b for b in filtered if b["pages"] > p]
        except:
            messagebox.showerror("Ошибка", "Количество страниц для фильтра должно быть числом!")
            return
    
    if not filtered:
        messagebox.showinfo("Результат", "Книги не найдены!")
    
    update_table(filtered)

def reset_filter():
    genre_filter_entry.delete(0, tk.END)
    pages_filter_entry.delete(0, tk.END)
    update_table()

def show_all():
    reset_filter()

# Окно
root = tk.Tk()
root.title("Book Tracker")
root.geometry("750x550")

# Заголовок
tk.Label(root, text="МОЯ БИБЛИОТЕКА", font=("Arial", 16, "bold")).pack(pady=10)

# ===== Рамка для добавления =====
add_frame = tk.LabelFrame(root, text="ДОБАВИТЬ КНИГУ", font=("Arial", 10, "bold"))
add_frame.pack(fill="x", padx=10, pady=5)

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

# ===== Рамка для фильтров =====
filter_frame = tk.LabelFrame(root, text="ФИЛЬТРАЦИЯ", font=("Arial", 10, "bold"))
filter_frame.pack(fill="x", padx=10, pady=5)

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

# ===== Таблица =====
table_frame = tk.LabelFrame(root, text="СПИСОК КНИГ", font=("Arial", 10, "bold"))
table_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("Название", "Автор", "Жанр", "Страниц")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

tree.heading("Название", text="Название")
tree.heading("Автор", text="Автор")
tree.heading("Жанр", text="Жанр")
tree.heading("Страниц", text="Страниц")

tree.column("Название", width=250)
tree.column("Автор", width=130)
tree.column("Жанр", width=110)
tree.column("Страниц", width=80)

scroll = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)

tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
scroll.pack(side="right", fill="y", pady=5)

# ===== Кнопка удаления =====
tk.Button(root, text="УДАЛИТЬ ВЫБРАННУЮ КНИГУ", command=delete_book, bg="red", fg="white").pack(pady=10)

# Показываем таблицу
update_table()
root.mainloop()
