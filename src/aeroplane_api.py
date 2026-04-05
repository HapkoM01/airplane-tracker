import requests
import time
from typing import List, Dict, Any
from src.abstract_api import AbstractAPI


class AeroplaneAPI(AbstractAPI):
    """Класс для работы с API nominatim.openstreetmap.org и opensky-network.org"""

    def __init__(self):
        """Инициализация API"""
        self.__base_url_nominatim = "https://nominatim.openstreetmap.org/search"
        self.__base_url_opensky = "https://opensky-network.org/api/states/all"
        self.__is_connected = False
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def _connect(self) -> bool:
        """Приватный метод для проверки подключения к API"""
        try:
            response = requests.get(
                self.__base_url_opensky,
                headers=self.__headers,
                params={"lamin": 0, "lomin": 0, "lamax": 0, "lomax": 0},
                timeout=10
            )
            self.__is_connected = response.status_code == 200
            return self.__is_connected
        except requests.RequestException:
            self.__is_connected = False
            return False

    def __get_default_bounding_box(self, country: str) -> Dict[str, float]:
        """Возвращает предустановленные координаты для популярных стран"""
        default_boxes = {
            "russia": {"lat_min": 41.0, "lat_max": 82.0, "lon_min": 19.0, "lon_max": 180.0},
            "usa": {"lat_min": 24.0, "lat_max": 49.0, "lon_min": -125.0, "lon_max": -66.0},
            "united states": {"lat_min": 24.0, "lat_max": 49.0, "lon_min": -125.0, "lon_max": -66.0},
            "canada": {"lat_min": 41.0, "lat_max": 83.0, "lon_min": -141.0, "lon_max": -52.0},
            "germany": {"lat_min": 47.0, "lat_max": 55.0, "lon_min": 5.0, "lon_max": 15.0},
            "france": {"lat_min": 42.0, "lat_max": 51.0, "lon_min": -5.0, "lon_max": 8.0},
            "uk": {"lat_min": 50.0, "lat_max": 59.0, "lon_min": -8.0, "lon_max": 2.0},
            "united kingdom": {"lat_min": 50.0, "lat_max": 59.0, "lon_min": -8.0, "lon_max": 2.0},
            "china": {"lat_min": 18.0, "lat_max": 53.0, "lon_min": 73.0, "lon_max": 135.0},
            "japan": {"lat_min": 30.0, "lat_max": 45.0, "lon_min": 128.0, "lon_max": 146.0},
            "australia": {"lat_min": -39.0, "lat_max": -10.0, "lon_min": 113.0, "lon_max": 154.0},
            "brazil": {"lat_min": -33.0, "lat_max": 5.0, "lon_min": -73.0, "lon_max": -34.0},
            "india": {"lat_min": 8.0, "lat_max": 37.0, "lon_min": 68.0, "lon_max": 97.0},
            "italy": {"lat_min": 36.0, "lat_max": 47.0, "lon_min": 6.0, "lon_max": 19.0},
            "spain": {"lat_min": 36.0, "lat_max": 44.0, "lon_min": -9.0, "lon_max": 4.0},
        }

        country_lower = country.lower()
        if country_lower in default_boxes:
            print(f"Найдены предустановленные координаты для {country}")
            return default_boxes[country_lower]

        for key, box in default_boxes.items():
            if key in country_lower:
                print(f"Найдены предустановленные координаты для {country} (по ключу {key})")
                return box

        return {}

    def __get_country_bounding_box(self, country: str) -> Dict[str, float]:
        """Приватный метод для получения bounding box страны"""
        # Сначала пробуем получить из предустановленных координат
        default_bbox = self.__get_default_bounding_box(country)
        if default_bbox:
            return default_bbox

        # Если нет в предустановленных, пробуем API
        params = {
            "q": country,
            "format": "json",
            "limit": 1
        }

        try:
            response = requests.get(
                self.__base_url_nominatim,
                headers=self.__headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data:
                    bounding_box = data[0].get("boundingbox", [])
                    if len(bounding_box) == 4:
                        return {
                            "lat_min": float(bounding_box[0]),
                            "lat_max": float(bounding_box[1]),
                            "lon_min": float(bounding_box[2]),
                            "lon_max": float(bounding_box[3])
                        }
        except Exception as e:
            print(f"Ошибка получения координат: {e}")

        return {}

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """Метод для получения информации о самолетах по названию страны"""
        # Проверяем подключение
        if not self._connect():
            return []

        # Небольшая задержка
        time.sleep(0.5)

        # Получаем bounding box страны
        bbox = self.__get_country_bounding_box(country)
        if not bbox:
            print(f"Не удалось получить координаты для страны '{country}'")
            return []

        print(f"Bounding box: lat {bbox['lat_min']}-{bbox['lat_max']}, lon {bbox['lon_min']}-{bbox['lon_max']}")

        # Запрашиваем самолеты в bounding box
        params = {
            "lamin": bbox["lat_min"],
            "lamax": bbox["lat_max"],
            "lomin": bbox["lon_min"],
            "lomax": bbox["lon_max"]
        }

        try:
            response = requests.get(
                self.__base_url_opensky,
                headers=self.__headers,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            aeroplanes = []
            states = data.get("states", [])

            print(f"Получено {len(states)} записей от OpenSky API")

            for state in states:
                if state and len(state) > 9:
                    # Пропускаем записи без позывного
                    callsign = state[1].strip() if state[1] else None
                    if not callsign or len(callsign) < 3:
                        continue

                    # Пропускаем записи без страны
                    origin_country = state[2] if state[2] else None
                    if not origin_country:
                        continue

                    aeroplane = {
                        "icao24": state[0],
                        "callsign": callsign,
                        "origin_country": origin_country,
                        "longitude": state[5] if state[5] is not None else None,
                        "latitude": state[6] if state[6] is not None else None,
                        "altitude": state[7] if state[7] is not None else None,
                        "velocity": state[9] if state[9] is not None else None,
                        "vertical_rate": state[11] if len(state) > 11 and state[11] is not None else None
                    }
                    aeroplanes.append(aeroplane)

            print(f"Отфильтровано {len(aeroplanes)} самолетов")
            return aeroplanes

        except requests.RequestException as e:
            print(f"Ошибка запроса к OpenSky API: {e}")
            return []
        except Exception as e:
            print(f"Ошибка обработки данных: {e}")
            return []