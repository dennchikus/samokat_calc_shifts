from logic import (
    add_shift,
    calculate,
    delete_shift,
    get_all_shifts,
    get_date,
    get_int,
    init_db,
    update_shift
    )

init_db()
# 1. Загрузка данных при старте
all_shifts = get_all_shifts()

while True:
    print("""
1. Добавить смену
2. Показать статистику
3. Удалить смену
4. Редактировать смену
5. Выход
    """)

    ans = input("Выбери действие: ")

    if ans == "1":
        
        date = get_date("Дата смены (ДД-ММ-ГГГГ) >> ")
        hours = get_int("Сколько часов длилась смена >> ")
        stops = get_int("Сколько стопов развез >> ")
        sli30 = get_int("Сколько из них SLI30 >> ")
        weather_bonus = get_int("Была ли надбавка за погоду?(Если да, то напиши сколько, иначе '0') >> ")

        add_shift(date, hours, stops, sli30, weather_bonus)
        print("✔ Смена сохранена!")

    elif ans == "2":
        sum_money = 0
        sum_hours = 0
        all_shifts = get_all_shifts()
        # Давай вместо простого принта попробуем вывести красиво?
        print("\n--- ТВОИ СМЕНЫ ---")
        one_shift = 0
        for shift in all_shifts:
            one_shift = calculate(shift)
            print("=" * 50)
            print(f"ID: {shift['id']} | Дата: {shift['date']} | Часов: {shift['hours']} | Стопов: {shift['stops']}")
            print(f"Заработал за смену: {one_shift} руб.")
            print("=" * 50)

            sum_money += one_shift
            sum_hours += shift['hours']
        print(f'ИТОГО ЗАРАБОТАНО: {str(sum_money)} руб.')
        print(f'ИТОГО ПРОРАБОТАНО: {str(sum_hours)} ч.')

    elif ans == "3":
        id_to_del = get_int("Введите ID смены для удаления >> ")
        if delete_shift(id_to_del):
            print("✔ Смена удалена!")
        else:
            print("Такой смены не существует")

    elif ans == "4":
        id_to_upd = get_int("Введите ID смены для редактирования >> ")
        new_hrs = get_int("Сколько часов длилась смена >> ")
        new_stops = get_int("Сколько стопов развез >> ")
        new_sli30 = get_int("Сколько из них SLI30 >> ")
        new_whrbns = get_int("Была ли надбавка за погоду?(Если да, то напиши сколько, иначе '0') >> ")

        if update_shift(id_to_upd, new_hrs, new_stops, new_sli30, new_whrbns):
            print("✔ Смена успешно изменена!")
        else:
            print("❌ Ошибка: Смена не найдена.")

    elif ans == "5":
        break
    else:
        print("")
        print("<< Ошибка ввода, выберите еще раз >>")

