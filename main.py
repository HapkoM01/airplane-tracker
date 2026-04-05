import sys
import os

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.aeroplane_api import AeroplaneAPI
from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver
from src.utils import (
    filter_aeroplanes_by_country,
    filter_aeroplanes_by_altitude,
    sort_aeroplanes_by_altitude,
    get_top_aeroplanes,
    parse_altitude_range,
    print_aeroplanes
)


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("\n" + "=" * 60)
    print("✈️ ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ ОТСЛЕЖИВАНИЯ САМОЛЕТОВ ✈️")
    print("=" * 60)

    # Создаем экземпляры классов
    api = AeroplaneAPI()
    saver = JSONSaver()

    while True:
        print("\n📋 Доступные команды:")
        print("1️⃣  Поиск самолетов по стране")
        print("2️⃣  Показать топ N самолетов по высоте")
        print("3️⃣  Фильтр по стране регистрации")
        print("4️⃣  Фильтр по диапазону высот")
        print("5️⃣  Показать все сохраненные самолеты")
        print("0️⃣  Выход")

        choice = input("\n👉 Выберите действие (0-5): ").strip()

        if choice == "0":
            print("\n👋 До свидания! Спасибо за использование системы!")
            break

        elif choice == "1":
            country = input("\n🌍 Введите название страны: ").strip()
            if not country:
                print("❌ Название страны не может быть пустым!")
                continue

            print(f"\n🔍 Поиск самолетов в воздушном пространстве {country}...")
            aeroplanes_data = api.get_aeroplanes(country)

            if not aeroplanes_data:
                print(
                    "❌ Не удалось получить данные о самолетах. Проверьте название страны или подключение к интернету.")
                continue

            aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

            # Сохраняем в файл
            for aeroplane in aeroplanes:
                saver.add_aeroplane(aeroplane)

            print(f"\n✅ Найдено {len(aeroplanes)} самолетов! Данные сохранены.")
            print_aeroplanes(aeroplanes)

        elif choice == "2":
            try:
                top_n = int(input("\n📊 Введите количество самолетов для топа: ").strip())
                if top_n <= 0:
                    print("❌ Количество должно быть положительным числом!")
                    continue
            except ValueError:
                print("❌ Введите корректное число!")
                continue

            all_aeroplanes = saver.get_all_aeroplanes()
            if not all_aeroplanes:
                print("❌ Нет сохраненных данных о самолетах. Сначала выполните поиск по стране.")
                continue

            sorted_aeroplanes = sort_aeroplanes_by_altitude(all_aeroplanes, reverse=True)
            top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)

            print(f"\n🏆 Топ {top_n} самолетов по высоте полета:")
            print_aeroplanes(top_aeroplanes)

        elif choice == "3":
            country = input("\n🌍 Введите страну регистрации: ").strip()
            if not country:
                print("❌ Название страны не может быть пустым!")
                continue

            all_aeroplanes = saver.get_all_aeroplanes()
            if not all_aeroplanes:
                print("❌ Нет сохраненных данных о самолетах. Сначала выполните поиск по стране.")
                continue

            filtered = filter_aeroplanes_by_country(all_aeroplanes, country)

            print(f"\n✈️ Самолеты, зарегистрированные в стране '{country}':")
            print_aeroplanes(filtered)

        elif choice == "4":
            altitude_range = input("\n📏 Введите диапазон высот (например: 10000-20000 или 15000): ").strip()
            if not altitude_range:
                print("❌ Диапазон не может быть пустым!")
                continue

            min_alt, max_alt = parse_altitude_range(altitude_range)
            if min_alt is None:
                print("❌ Неверный формат диапазона! Используйте формат: 10000-20000")
                continue

            all_aeroplanes = saver.get_all_aeroplanes()
            if not all_aeroplanes:
                print("❌ Нет сохраненных данных о самолетах. Сначала выполните поиск по стране.")
                continue

            filtered = filter_aeroplanes_by_altitude(all_aeroplanes, min_alt, max_alt)

            if min_alt == max_alt:
                print(f"\n📏 Самолеты на высоте {min_alt:.0f} м:")
            else:
                print(f"\n📏 Самолеты в диапазоне высот {min_alt:.0f} - {max_alt:.0f} м:")
            print_aeroplanes(filtered)

        elif choice == "5":
            all_aeroplanes = saver.get_all_aeroplanes()
            if not all_aeroplanes:
                print("❌ Нет сохраненных данных о самолетах. Сначала выполните поиск по стране.")
                continue

            print("\n📚 ВСЕ СОХРАНЕННЫЕ САМОЛЕТЫ:")
            print_aeroplanes(all_aeroplanes)

        else:
            print("❌ Неверный выбор! Пожалуйста, выберите действие от 0 до 5.")


if __name__ == "__main__":
    user_interaction()
