import sys
import os
import pytest
from unittest.mock import Mock, patch
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.aeroplane_api import AeroplaneAPI


class TestAeroplaneAPI:
    """Тесты для AeroplaneAPI"""

    @pytest.fixture
    def api(self):
        """Фикстура для API"""
        return AeroplaneAPI()

    def test_initialization(self, api):
        """Тест инициализации API"""
        assert api is not None
        assert api._AeroplaneAPI__base_url_nominatim == "https://nominatim.openstreetmap.org/search"
        assert api._AeroplaneAPI__base_url_opensky == "https://opensky-network.org/api/states/all"

    def test_connect_success(self, api):
        """Тест успешного подключения"""
        with patch('src.aeroplane_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            result = api._connect()
            assert result is True

    def test_connect_failure_http_error(self, api):
        """Тест неудачного подключения - HTTP ошибка 404"""
        with patch('src.aeroplane_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            result = api._connect()
            assert result is False

    def test_connect_failure_http_500(self, api):
        """Тест неудачного подключения - HTTP ошибка 500"""
        with patch('src.aeroplane_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_get.return_value = mock_response

            result = api._connect()
            assert result is False

    def test_connect_failure_exception(self, api):
        """Тест неудачного подключения - исключение RequestException"""
        with patch('src.aeroplane_api.requests.get') as mock_get:
            # Используем requests.RequestException вместо обычного Exception
            mock_get.side_effect = requests.RequestException("Connection error")

            result = api._connect()
            assert result is False

    def test_connect_failure_timeout(self, api):
        """Тест неудачного подключения - таймаут"""
        with patch('src.aeroplane_api.requests.get') as mock_get:
            # Используем requests.Timeout (наследник RequestException)
            mock_get.side_effect = requests.Timeout("Timeout error")

            result = api._connect()
            assert result is False

    def test_get_default_bounding_box(self, api):
        """Тест получения предустановленных координат"""
        # Тест для известной страны
        bbox = api._AeroplaneAPI__get_default_bounding_box("Japan")
        assert bbox is not None
        assert "lat_min" in bbox
        assert "lat_max" in bbox
        assert "lon_min" in bbox
        assert "lon_max" in bbox
        assert bbox["lat_min"] == 30.0
        assert bbox["lat_max"] == 45.0

        # Тест для неизвестной страны
        bbox = api._AeroplaneAPI__get_default_bounding_box("UnknownCountryXYZ")
        assert bbox == {}

        # Тест для страны с частичным совпадением
        bbox = api._AeroplaneAPI__get_default_bounding_box("United States of America")
        assert bbox is not None
        assert "lat_min" in bbox

    def test_get_country_bounding_box_from_default(self, api):
        """Тест получения bounding box из предустановленных координат"""
        bbox = api._AeroplaneAPI__get_country_bounding_box("Japan")
        assert bbox is not None
        assert bbox["lat_min"] == 30.0
        assert bbox["lat_max"] == 45.0
        assert bbox["lon_min"] == 128.0
        assert bbox["lon_max"] == 146.0

    def test_get_country_bounding_box_from_api(self, api):
        """Тест получения bounding box через API"""
        with patch('src.aeroplane_api.requests.get') as mock_get:
            # Мокаем успешный ответ от Nominatim
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [{
                "boundingbox": ["40.0", "50.0", "10.0", "20.0"]
            }]
            mock_get.return_value = mock_response

            bbox = api._AeroplaneAPI__get_country_bounding_box("TestCountry")
            assert bbox is not None
            assert bbox["lat_min"] == 40.0
            assert bbox["lat_max"] == 50.0
            assert bbox["lon_min"] == 10.0
            assert bbox["lon_max"] == 20.0

    def test_get_country_bounding_box_api_fails(self, api):
        """Тест ошибки API при получении bounding box"""
        with patch('src.aeroplane_api.requests.get') as mock_get:
            mock_get.side_effect = requests.RequestException("API Error")

            bbox = api._AeroplaneAPI__get_country_bounding_box("TestCountry")
            assert bbox == {}

    def test_get_country_bounding_box_api_403(self, api):
        """Тест ошибки 403 при получении bounding box"""
        with patch('src.aeroplane_api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 403
            mock_get.return_value = mock_response

            bbox = api._AeroplaneAPI__get_country_bounding_box("TestCountry")
            assert bbox == {}

    def test_get_aeroplanes_success(self, api):
        """Тест успешного получения самолетов"""
        with patch('src.aeroplane_api.AeroplaneAPI._connect') as mock_connect, \
                patch('src.aeroplane_api.AeroplaneAPI._AeroplaneAPI__get_country_bounding_box') as mock_get_bbox, \
                patch('src.aeroplane_api.requests.get') as mock_get:
            mock_connect.return_value = True
            mock_get_bbox.return_value = {
                "lat_min": 30.0,
                "lat_max": 45.0,
                "lon_min": 128.0,
                "lon_max": 146.0
            }

            # Мокаем успешный ответ от OpenSky
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "states": [
                    ["abc123", "AAL101", "United States", None, None, -73.5, 40.7, 11250, None, 245.5, None, None,
                     None],
                    ["def456", "BAW202", "United Kingdom", None, None, -0.5, 51.5, 9800, None, 230.0, None, None, None],
                ]
            }
            mock_get.return_value = mock_response

            result = api.get_aeroplanes("Japan")

            assert len(result) == 2
            assert result[0]["callsign"] == "AAL101"
            assert result[1]["callsign"] == "BAW202"

    def test_get_aeroplanes_no_connection(self, api):
        """Тест получения самолетов без подключения"""
        with patch('src.aeroplane_api.AeroplaneAPI._connect') as mock_connect:
            mock_connect.return_value = False

            result = api.get_aeroplanes("USA")
            assert result == []

    def test_get_aeroplanes_no_bounding_box(self, api):
        """Тест получения самолетов без bounding box"""
        with patch('src.aeroplane_api.AeroplaneAPI._connect') as mock_connect, \
                patch('src.aeroplane_api.AeroplaneAPI._AeroplaneAPI__get_country_bounding_box') as mock_get_bbox:
            mock_connect.return_value = True
            mock_get_bbox.return_value = {}

            result = api.get_aeroplanes("UnknownCountry")
            assert result == []

    def test_get_aeroplanes_api_error(self, api):
        """Тест ошибки API при получении самолетов"""
        with patch('src.aeroplane_api.AeroplaneAPI._connect') as mock_connect, \
                patch('src.aeroplane_api.AeroplaneAPI._AeroplaneAPI__get_country_bounding_box') as mock_get_bbox, \
                patch('src.aeroplane_api.requests.get') as mock_get:
            mock_connect.return_value = True
            mock_get_bbox.return_value = {
                "lat_min": 30.0,
                "lat_max": 45.0,
                "lon_min": 128.0,
                "lon_max": 146.0
            }
            mock_get.side_effect = requests.RequestException("API Error")

            result = api.get_aeroplanes("Japan")
            assert result == []

    def test_get_aeroplanes_with_empty_states(self, api):
        """Тест получения самолетов с пустым ответом"""
        with patch('src.aeroplane_api.AeroplaneAPI._connect') as mock_connect, \
                patch('src.aeroplane_api.AeroplaneAPI._AeroplaneAPI__get_country_bounding_box') as mock_get_bbox, \
                patch('src.aeroplane_api.requests.get') as mock_get:
            mock_connect.return_value = True
            mock_get_bbox.return_value = {
                "lat_min": 30.0,
                "lat_max": 45.0,
                "lon_min": 128.0,
                "lon_max": 146.0
            }

            # Мокаем ответ без самолетов
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"states": []}
            mock_get.return_value = mock_response

            result = api.get_aeroplanes("Japan")
            assert result == []

    def test_get_aeroplanes_with_http_error(self, api):
        """Тест HTTP ошибки при получении самолетов"""
        with patch('src.aeroplane_api.AeroplaneAPI._connect') as mock_connect, \
                patch('src.aeroplane_api.AeroplaneAPI._AeroplaneAPI__get_country_bounding_box') as mock_get_bbox, \
                patch('src.aeroplane_api.requests.get') as mock_get:
            mock_connect.return_value = True
            mock_get_bbox.return_value = {
                "lat_min": 30.0,
                "lat_max": 45.0,
                "lon_min": 128.0,
                "lon_max": 146.0
            }

            # Мокаем HTTP ошибку
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.RequestException("HTTP 500 Error")
            mock_get.return_value = mock_response

            result = api.get_aeroplanes("Japan")
            assert result == []
