from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect(self) -> bool:
        """Приватный метод для подключения к API"""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """Метод для получения информации о самолетах по названию страны"""
        pass
