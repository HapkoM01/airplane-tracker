from typing import Optional


class Aeroplane:
    """Класс для работы с информацией о самолетах"""

    __slots__ = ("__callsign", "__origin_country", "__altitude", "__velocity", "__longitude", "__latitude")

    def __init__(self, callsign: str, origin_country: str, altitude: Optional[float],
                 velocity: Optional[float], longitude: Optional[float] = None,
                 latitude: Optional[float] = None):
        """Инициализация самолета"""
        self.__callsign = self.__validate_callsign(callsign)
        self.__origin_country = self.__validate_country(origin_country)
        self.__altitude = self.__validate_altitude(altitude)
        self.__velocity = self.__validate_velocity(velocity)
        self.__longitude = longitude
        self.__latitude = latitude

    @property
    def callsign(self) -> str:
        """Геттер для позывного"""
        return self.__callsign

    @property
    def origin_country(self) -> str:
        """Геттер для страны регистрации"""
        return self.__origin_country

    @property
    def altitude(self) -> Optional[float]:
        """Геттер для высоты полета"""
        return self.__altitude

    @property
    def velocity(self) -> Optional[float]:
        """Геттер для скорости полета"""
        return self.__velocity

    @property
    def longitude(self) -> Optional[float]:
        """Геттер для долготы"""
        return self.__longitude

    @property
    def latitude(self) -> Optional[float]:
        """Геттер для широты"""
        return self.__latitude

    def __validate_callsign(self, callsign: str) -> str:
        """Приватный метод валидации позывного"""
        if not callsign or not isinstance(callsign, str):
            return "Unknown"
        return callsign.strip()

    def __validate_country(self, country: str) -> str:
        """Приватный метод валидации страны"""
        if not country or not isinstance(country, str):
            return "Unknown"
        return country.strip()

    def __validate_altitude(self, altitude: Optional[float]) -> Optional[float]:
        """Приватный метод валидации высоты"""
        if altitude is None:
            return None
        try:
            altitude = float(altitude)
            return altitude if altitude >= 0 else None
        except (ValueError, TypeError):
            return None

    def __validate_velocity(self, velocity: Optional[float]) -> Optional[float]:
        """Приватный метод валидации скорости"""
        if velocity is None:
            return None
        try:
            velocity = float(velocity)
            return velocity if velocity >= 0 else None
        except (ValueError, TypeError):
            return None

    def __eq__(self, other) -> bool:
        """Сравнение самолетов по высоте (равенство)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__altitude == other.__altitude

    def __lt__(self, other) -> bool:
        """Сравнение самолетов по высоте (меньше)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.__altitude is None and other.__altitude is None:
            return False
        if self.__altitude is None:
            return True
        if other.__altitude is None:
            return False
        return self.__altitude < other.__altitude

    def __le__(self, other) -> bool:
        """Сравнение самолетов по высоте (меньше или равно)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self < other or self == other

    def __gt__(self, other) -> bool:
        """Сравнение самолетов по высоте (больше)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return other < self

    def __ge__(self, other) -> bool:
        """Сравнение самолетов по высоте (больше или равно)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return other <= self

    def __str__(self) -> str:
        """Строковое представление самолета"""
        altitude_str = f"{self.__altitude:.0f} м" if self.__altitude else "неизвестно"
        velocity_str = f"{self.__velocity:.0f} м/с" if self.__velocity else "неизвестно"
        return (f"✈️ {self.__callsign} | Страна: {self.__origin_country} | "
                f"Высота: {altitude_str} | Скорость: {velocity_str}")

    def to_dict(self) -> dict:
        """Преобразование самолета в словарь"""
        return {
            "callsign": self.__callsign,
            "origin_country": self.__origin_country,
            "altitude": self.__altitude,
            "velocity": self.__velocity,
            "longitude": self.__longitude,
            "latitude": self.__latitude
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Aeroplane":
        """Создание самолета из словаря"""
        return cls(
            callsign=data.get("callsign", "Unknown"),
            origin_country=data.get("origin_country", "Unknown"),
            altitude=data.get("altitude"),
            velocity=data.get("velocity"),
            longitude=data.get("longitude"),
            latitude=data.get("latitude")
        )

    @classmethod
    def cast_to_object_list(cls, aeroplanes_data: list) -> list:
        """Преобразование списка словарей в список объектов"""
        aeroplanes = []
        for data in aeroplanes_data:
            if data and data.get("callsign"):
                aeroplane = cls(
                    callsign=data.get("callsign", "Unknown"),
                    origin_country=data.get("origin_country", "Unknown"),
                    altitude=data.get("altitude"),
                    velocity=data.get("velocity"),
                    longitude=data.get("longitude"),
                    latitude=data.get("latitude")
                )
                aeroplanes.append(aeroplane)
        return aeroplanes
