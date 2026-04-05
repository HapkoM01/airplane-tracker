import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from abc import ABC, abstractmethod
from src.abstract_api import AbstractAPI
from src.abstract_file_saver import AbstractFileSaver


def test_abstract_api_is_abstract():
    """Тест, что AbstractAPI является абстрактным"""
    assert issubclass(AbstractAPI, ABC)
    assert hasattr(AbstractAPI, '_connect')
    assert hasattr(AbstractAPI, 'get_aeroplanes')


def test_abstract_file_saver_is_abstract():
    """Тест, что AbstractFileSaver является абстрактным"""
    assert issubclass(AbstractFileSaver, ABC)
    assert hasattr(AbstractFileSaver, 'add_aeroplane')
    assert hasattr(AbstractFileSaver, 'get_aeroplanes')
    assert hasattr(AbstractFileSaver, 'delete_aeroplane')


def test_cannot_instantiate_abstract_api():
    """Тест, что нельзя создать экземпляр абстрактного класса"""
    with pytest.raises(TypeError):
        AbstractAPI()


def test_cannot_instantiate_abstract_file_saver():
    """Тест, что нельзя создать экземпляр абстрактного класса"""
    with pytest.raises(TypeError):
        AbstractFileSaver()
