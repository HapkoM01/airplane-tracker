import sys
import os
import json
import tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.json_saver import JSONSaver
from src.aeroplane import Aeroplane


@pytest.fixture
def temp_json_file():
    """Фикстура для временного JSON файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name

    yield temp_file

    # Очистка после тестов
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def sample_aeroplane():
    """Фикстура с тестовым самолетом"""
    return Aeroplane("TEST123", "USA", 10000, 250, 10.0, 20.0)


def test_json_saver_initialization():
    """Тест инициализации JSONSaver"""
    saver = JSONSaver()
    assert saver is not None
    assert saver._JSONSaver__filename == "data/aeroplanes.json"


def test_add_aeroplane(temp_json_file, sample_aeroplane):
    """Тест добавления самолета"""
    saver = JSONSaver(filename=temp_json_file)

    saver.add_aeroplane(sample_aeroplane)

    # Проверяем, что файл создан и содержит данные
    assert os.path.exists(temp_json_file)

    with open(temp_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["callsign"] == "TEST123"


def test_add_duplicate_aeroplane(temp_json_file, sample_aeroplane):
    """Тест добавления дубликата самолета"""
    saver = JSONSaver(filename=temp_json_file)

    saver.add_aeroplane(sample_aeroplane)
    saver.add_aeroplane(sample_aeroplane)

    with open(temp_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Дубликат не должен добавиться
    assert len(data) == 1


def test_get_aeroplanes(temp_json_file):
    """Тест получения всех самолетов"""
    saver = JSONSaver(filename=temp_json_file)

    a1 = Aeroplane("A1", "USA", 10000, 200)
    a2 = Aeroplane("A2", "Canada", 15000, 250)

    saver.add_aeroplane(a1)
    saver.add_aeroplane(a2)

    aeroplanes = saver.get_aeroplanes()
    assert len(aeroplanes) == 2


def test_get_aeroplanes_filter_by_country(temp_json_file):
    """Тест фильтрации по стране"""
    saver = JSONSaver(filename=temp_json_file)

    a1 = Aeroplane("A1", "USA", 10000, 200)
    a2 = Aeroplane("A2", "Canada", 15000, 250)
    a3 = Aeroplane("A3", "USA", 12000, 220)

    saver.add_aeroplane(a1)
    saver.add_aeroplane(a2)
    saver.add_aeroplane(a3)

    usa_planes = saver.get_aeroplanes(origin_country="USA")
    assert len(usa_planes) == 2
    assert all(p.origin_country == "USA" for p in usa_planes)


def test_get_aeroplanes_filter_by_altitude(temp_json_file):
    """Тест фильтрации по высоте"""
    saver = JSONSaver(filename=temp_json_file)

    a1 = Aeroplane("A1", "USA", 10000, 200)
    a2 = Aeroplane("A2", "Canada", 15000, 250)
    a3 = Aeroplane("A3", "USA", 20000, 300)

    saver.add_aeroplane(a1)
    saver.add_aeroplane(a2)
    saver.add_aeroplane(a3)

    high_planes = saver.get_aeroplanes(min_altitude=15000)
    assert len(high_planes) == 2
    assert all(p.altitude >= 15000 for p in high_planes)

    low_planes = saver.get_aeroplanes(max_altitude=12000)
    assert len(low_planes) == 1
    assert low_planes[0].altitude <= 12000


def test_get_aeroplanes_filter_by_altitude_range(temp_json_file):
    """Тест фильтрации по диапазону высот"""
    saver = JSONSaver(filename=temp_json_file)

    a1 = Aeroplane("A1", "USA", 10000, 200)
    a2 = Aeroplane("A2", "Canada", 15000, 250)
    a3 = Aeroplane("A3", "USA", 20000, 300)

    saver.add_aeroplane(a1)
    saver.add_aeroplane(a2)
    saver.add_aeroplane(a3)

    range_planes = saver.get_aeroplanes(min_altitude=12000, max_altitude=18000)
    assert len(range_planes) == 1
    assert range_planes[0].callsign == "A2"


def test_delete_aeroplane(temp_json_file, sample_aeroplane):
    """Тест удаления самолета"""
    saver = JSONSaver(filename=temp_json_file)

    saver.add_aeroplane(sample_aeroplane)
    assert len(saver.get_aeroplanes()) == 1

    saver.delete_aeroplane(sample_aeroplane)
    assert len(saver.get_aeroplanes()) == 0


def test_get_all_aeroplanes(temp_json_file):
    """Тест получения всех самолетов"""
    saver = JSONSaver(filename=temp_json_file)

    a1 = Aeroplane("A1", "USA", 10000, 200)
    a2 = Aeroplane("A2", "Canada", 15000, 250)

    saver.add_aeroplane(a1)
    saver.add_aeroplane(a2)

    all_planes = saver.get_all_aeroplanes()
    assert len(all_planes) == 2
