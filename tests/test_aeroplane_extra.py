import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.aeroplane import Aeroplane


def test_aeroplane_comparison_with_none():
    """Тест сравнения с None"""
    a1 = Aeroplane("A1", "USA", 10000, 200)
    a2 = Aeroplane("A2", "USA", None, 200)
    a3 = Aeroplane("A3", "USA", None, 200)

    # Сравнение с None
    assert a1 > a2
    assert a2 < a1
    assert not (a2 > a3)
    assert a2 == a3
    assert a2 >= a3
    assert a2 <= a3


def test_aeroplane_validation_edge_cases():
    """Тест валидации с краевыми случаями"""
    # Проверка с нулевыми значениями
    a1 = Aeroplane("Test", "Test", 0, 0)
    assert a1.altitude == 0
    assert a1.velocity == 0

    # Проверка с некорректными типами
    a2 = Aeroplane(123, 456, "invalid", "invalid")
    assert a2.callsign == "Unknown"
    assert a2.origin_country == "Unknown"
    assert a2.altitude is None
    assert a2.velocity is None


def test_aeroplane_lt_with_none():
    """Тест сравнения меньше с None"""
    a1 = Aeroplane("A1", "USA", 10000, 200)
    a2 = Aeroplane("A2", "USA", None, 200)
    a3 = Aeroplane("A3", "USA", None, 200)

    assert a2 < a1
    assert not (a1 < a2)
    assert not (a2 < a3)  # оба None -> False


def test_aeroplane_str_with_none():
    """Тест строкового представления с None"""
    a1 = Aeroplane("Test", "Test", None, None)
    str_repr = str(a1)
    assert "неизвестно" in str_repr


def test_aeroplane_eq_with_different_type():
    """Тест сравнения с объектом другого типа"""
    a1 = Aeroplane("A1", "USA", 10000, 200)
    assert a1.__eq__("not a plane") == NotImplemented
