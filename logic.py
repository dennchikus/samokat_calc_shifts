import json
import os
import re
import sqlite3

def init_db():
    # 1. Подключаемся к файлу (если его нет, он создастся сам)
    conn = sqlite3.connect("work.db")
    
    # 2. Создаем курсор — это наш "исполнитель"
    cursor = conn.cursor()
    
    # 3. Пишем команду на языке SQL
    # Мы говорим: "Создай таблицу, ЕСЛИ ЕЁ ЕЩЕ НЕТ"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            hours INTEGER,
            stops INTEGER,
            sli30 INTEGER,
            wtr_bns INTEGER
        )
    """)
    
    # 4. Сохраняем изменения
    conn.commit()
    
    # 5. Закрываем соединение
    conn.close()

def add_shift(date, hours, stops, sli30, weather_bonus):

    conn = sqlite3.connect("work.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO shifts (date, hours, stops, sli30, wtr_bns)
        VALUES (?, ?, ?, ?, ?)
    """, (date, hours, stops, sli30, weather_bonus))

    conn.commit()
    conn.close()

def calculate(shift):
    return (shift['hours'] * 110) + (shift['stops'] * (45 + shift['wtr_bns'])) + (shift['sli30'] * 15)

def get_all_shifts():
    conn = sqlite3.connect("work.db")
    # Магия: говорим базе возвращать данные в виде "имя колонки: значение"
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM shifts")
    rows = cursor.fetchall()
    
    # Превращаем результат в привычный список словарей
    shifts = [dict(row) for row in rows]
    
    conn.close()
    return shifts

def delete_shift(shift_id):
    conn = sqlite3.connect("work.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM shifts WHERE id = ?", (shift_id,))
    
    # Проверяем, удалилось ли хоть что-то
    deleted_rows = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    # Если удаленных строк больше 0, возвращаем True, иначе False
    return deleted_rows > 0

def update_shift(shift_id, hours, stops, sli30, weather_bonus):
    conn = sqlite3.connect("work.db")
    cursor = conn.cursor()
    
    # Сеттим (устанавливаем) новые значения там, где совпал ID
    cursor.execute("""
        UPDATE shifts 
        SET hours = ?, stops = ?, sli30 = ?, wtr_bns = ?
        WHERE id = ?
    """, (hours, stops, sli30, weather_bonus, shift_id))
    
    updated_rows = cursor.rowcount
    conn.commit()
    conn.close()
    
    return updated_rows > 0


def get_int(message):
    while True:
        try:
            n = int(input(message))
            if n < 0:
                print("Число не может быть отрицательным. Попробуй еще раз.")
                continue  # Возвращаемся в начало цикла
            return n
        except ValueError:
            print("Введено неверное значение, введи целое число.")

def get_date(message):
    date_mask = r"\d{2}-\d{2}-\d{4}"
    while 1:
        date_inp = input(message)
        if re.fullmatch(date_mask, date_inp):
            return date_inp
        else:
            print("Неверный формат даты, введи ДД-ММ-ГГГГ")


# Старая версия 
# def load_shifts():
#     if os.path.exists("shifts.json"):
#         with open("shifts.json", "r", encoding="utf-8") as f:
#             all_shifts = json.load(f)
#     else:
#         all_shifts = []
#     return all_shifts

# def save_json(array):
#     with open("shifts.json", "w", encoding="utf-8") as f:
#         json.dump(array, f, ensure_ascii=False, indent=4)

# def delete_last_shift(shifts):
#     if len(shifts) != 0:
#         shifts.pop()
#         save_json(shifts)
#         return True
#     else:
#         return False




