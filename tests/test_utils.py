import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.aeroplane import Aeroplane
from src.utils import (
    filter_aeroplanes_by_country,
    filter_aeroplanes_by_altitude,
    sort_aeroplanes_by_altitude,
    get_top_aeroplanes,
    parse_altitude_range,
)


@pytest.fixture
def sample_aeroplanes():
    """Фикстура с тестовыми самолетами"""
    return [
        Aeroplane("A1", "USA", 10000, 200),      # высота 10000
        Aeroplane("A2", "Canada", 15000, 250),   # высота 15000
        Aeroplane("A3", "USA", 8000, 180),       # высота 8000
        Aeroplane("A4", "Russia", 20000, 300),   # высота 20000
        Aeroplane("A5", "USA", None, None)       # высота неизвестна
    ]


def test_filter_by_country(sample_aeroplanes):
    """Тест фильтрации по стране"""
    filtered = filter_aeroplanes_by_country(sample_aeroplanes, "USA")
    assert len(filtered) == 3  # A1, A3, A5
    assert all(a.origin_country == "USA" for a in filtered)


def test_filter_by_altitude(sample_aeroplanes):
    """Тест фильтрации по высоте"""
    filtered = filter_aeroplanes_by_altitude(sample_aeroplanes, min_altitude=10000)
    assert len(filtered) == 3  # A1(10000), A2(15000), A4(20000)
    assert all(a.altitude >= 10000 for a in filtered)


def test_filter_by_altitude_range(sample_aeroplanes):
    """Тест фильтрации по диапазону высот"""
    filtered = filter_aeroplanes_by_altitude(sample_aeroplanes, min_altitude=9000, max_altitude=16000)
    assert len(filtered) == 2  # A1(10000), A2(15000)


def test_sort_by_altitude(sample_aeroplanes):
    """Тест сортировки по высоте"""
    sorted_asc = sort_aeroplanes_by_altitude(sample_aeroplanes)
    sorted_desc = sort_aeroplanes_by_altitude(sample_aeroplanes, reverse=True)

    # Самолеты с неизвестной высотой должны быть в начале при сортировке по возрастанию
    assert sorted_asc[0].altitude is None
    # Самолеты с неизвестной высотой должны быть в конце при сортировке по убыванию
    assert sorted_desc[-1].altitude is None


def test_get_top_aeroplanes(sample_aeroplanes):
    """Тест получения топ N самолетов"""
    top = get_top_aeroplanes(sample_aeroplanes, 3)
    assert len(top) == 3
    assert top[0].callsign == "A1"


def test_parse_altitude_range():
    """Тест парсинга диапазона высот"""
    min_alt, max_alt = parse_altitude_range("10000-20000")
    assert min_alt == 10000
    assert max_alt == 20000

    min_alt, max_alt = parse_altitude_range("15000")
    assert min_alt == 15000
    assert max_alt == 15000

    min_alt, max_alt = parse_altitude_range("invalid")
    assert min_alt is None
    assert max_alt is None


def test_filter_by_altitude_min_only(sample_aeroplanes):
    """Тест фильтрации только по минимальной высоте"""
    filtered = filter_aeroplanes_by_altitude(sample_aeroplanes, min_altitude=15000)
    assert len(filtered) == 2  # A2(15000), A4(20000)


def test_filter_by_altitude_max_only(sample_aeroplanes):
    """Тест фильтрации только по максимальной высоте"""
    filtered = filter_aeroplanes_by_altitude(sample_aeroplanes, max_altitude=12000)
    assert len(filtered) == 2  # A1(10000), A3(8000)


def test_filter_by_altitude_no_filter(sample_aeroplanes):
    """Тест фильтрации без параметров"""
    filtered = filter_aeroplanes_by_altitude(sample_aeroplanes)
    assert len(filtered) == 5
