import json
import os
from typing import List, Optional
from src.abstract_file_saver import AbstractFileSaver
from src.aeroplane import Aeroplane


class JSONSaver(AbstractFileSaver):
    """Класс для сохранения информации о самолетах в JSON-файл"""

    def __init__(self, filename: str = "data/aeroplanes.json"):
        """Инициализация JSON сохранителя"""
        self.__filename = filename
        self.__ensure_directory_exists()

    def __ensure_directory_exists(self) -> None:
        """Приватный метод для создания директории, если она не существует"""
        directory = os.path.dirname(self.__filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def __load_data(self) -> List[dict]:
        """Приватный метод для загрузки данных из файла"""
        if not os.path.exists(self.__filename):
            return []

        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def __save_data(self, data: List[dict]) -> None:
        """Приватный метод для сохранения данных в файл"""
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def __is_duplicate(self, aeroplane: Aeroplane, data: List[dict]) -> bool:
        """Приватный метод для проверки дубликатов"""
        for item in data:
            if item.get("callsign") == aeroplane.callsign:
                return True
        return False

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Метод для добавления информации о самолете в файл"""
        data = self.__load_data()

        if not self.__is_duplicate(aeroplane, data):
            data.append(aeroplane.to_dict())
            self.__save_data(data)

    def get_aeroplanes(self, **kwargs) -> List[Aeroplane]:
        """Метод для получения данных из файла по указанным критериям"""
        data = self.__load_data()
        aeroplanes = [Aeroplane.from_dict(item) for item in data]

        # Фильтрация по критериям
        if kwargs.get("origin_country"):
            origin_country = kwargs["origin_country"].lower()
            aeroplanes = [a for a in aeroplanes
                          if a.origin_country.lower() == origin_country]

        if kwargs.get("min_altitude") is not None:
            min_altitude = kwargs["min_altitude"]
            aeroplanes = [a for a in aeroplanes
                          if a.altitude is not None and a.altitude >= min_altitude]

        if kwargs.get("max_altitude") is not None:
            max_altitude = kwargs["max_altitude"]
            aeroplanes = [a for a in aeroplanes
                          if a.altitude is not None and a.altitude <= max_altitude]

        return aeroplanes

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Метод для удаления информации о самолете из файла"""
        data = self.__load_data()
        data = [item for item in data if item.get("callsign") != aeroplane.callsign]
        self.__save_data(data)

    def get_all_aeroplanes(self) -> List[Aeroplane]:
        """Метод для получения всех самолетов из файла"""
        return self.get_aeroplanes()
