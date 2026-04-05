from abc import ABC, abstractmethod
from typing import List
from src.aeroplane import Aeroplane


class AbstractFileSaver(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Метод для добавления информации о самолете в файл"""
        pass

    @abstractmethod
    def get_aeroplanes(self, **kwargs) -> List[Aeroplane]:
        """Метод для получения данных из файла по указанным критериям"""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Метод для удаления информации о самолете из файла"""
        pass
