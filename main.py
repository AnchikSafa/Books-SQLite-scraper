import requests
from bs4 import BeautifulSoup
import sqlite3

# 1. Подключаемся к базе данных SQLite (файл books_database.db создастся автоматически)
conn = sqlite3.connect("books_database.db")
cursor = conn.cursor()

# 2. Создаем таблицу для хранения данных, если её еще нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price TEXT
    )
''')
conn.commit()

# Счетчик для собранных книг
total_books = 0

# 3. Запускаем цикл по всем 50 страницам сайта
for page in range(1, 51):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    print(f"Сейчс парсим страницу {page}...")

    response = requests.get(url)

    # Если страница не найдена (например, сайт ответил ошибкой 404), прерываем цикл
    if response.status_code != 200:
        break

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим все книги на странице
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text

        # 4. Вставляем данные каждой книги в базу данных SQLite
        cursor.execute("INSERT INTO books (title, price) VALUES (?, ?)", (title, price))
        total_books += 1

# Сохраняем изменения и закрываем соединение с базой
conn.commit()
conn.close()

print(f"\nГотово! Успешно собрано и записано в базу данных книг: {total_books}")
print("Файл базы данных 'books_database.db' появился в папке твоего проекта.")