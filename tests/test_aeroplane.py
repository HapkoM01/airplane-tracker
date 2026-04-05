import pytest
from src.aeroplane import Aeroplane


def test_aeroplane_creation():
    """Тест создания самолета"""
    aeroplane = Aeroplane("UAL1621", "United States", 10203.18, 268.79)

    assert aeroplane.callsign == "UAL1621"
    assert aeroplane.origin_country == "United States"
    assert aeroplane.altitude == 10203.18
    assert aeroplane.velocity == 268.79


def test_aeroplane_validation():
    """Тест валидации данных"""
    aeroplane = Aeroplane("", "", -100, -50)

    assert aeroplane.callsign == "Unknown"
    assert aeroplane.origin_country == "Unknown"
    assert aeroplane.altitude is None
    assert aeroplane.velocity is None


def test_aeroplane_comparison():
    """Тест сравнения самолетов"""
    a1 = Aeroplane("A1", "USA", 10000, 200)
    a2 = Aeroplane("A2", "USA", 15000, 250)
    a3 = Aeroplane("A3", "USA", 10000, 200)

    assert a1 < a2
    assert a2 > a1
    assert a1 == a3
    assert a1 <= a3
    assert a2 >= a1


def test_aeroplane_to_dict():
    """Тест преобразования в словарь"""
    aeroplane = Aeroplane("UAL1621", "United States", 10203.18, 268.79, 10.0, 20.0)
    data = aeroplane.to_dict()

    assert data["callsign"] == "UAL1621"
    assert data["origin_country"] == "United States"
    assert data["altitude"] == 10203.18
    assert data["velocity"] == 268.79
    assert data["longitude"] == 10.0
    assert data["latitude"] == 20.0


def test_aeroplane_from_dict():
    """Тест создания из словаря"""
    data = {
        "callsign": "UAL1621",
        "origin_country": "United States",
        "altitude": 10203.18,
        "velocity": 268.79
    }
    aeroplane = Aeroplane.from_dict(data)

    assert aeroplane.callsign == "UAL1621"
    assert aeroplane.origin_country == "United States"
    assert aeroplane.altitude == 10203.18
    assert aeroplane.velocity == 268.79


def test_cast_to_object_list():
    """Тест преобразования списка словарей в список объектов"""
    data_list = [
        {"callsign": "A1", "origin_country": "USA", "altitude": 10000, "velocity": 200},
        {"callsign": "A2", "origin_country": "Canada", "altitude": 15000, "velocity": 250}
    ]

    aeroplanes = Aeroplane.cast_to_object_list(data_list)

    assert len(aeroplanes) == 2
    assert aeroplanes[0].callsign == "A1"
    assert aeroplanes[1].callsign == "A2"


def test_aeroplane_str():
    """Тест строкового представления"""
    aeroplane = Aeroplane("UAL1621", "United States", 10203.18, 268.79)
    str_repr = str(aeroplane)

    assert "UAL1621" in str_repr
    assert "United States" in str_repr
    assert "10203" in str_repr
    assert "269" in str_repr
