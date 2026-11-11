"""Тесты конфигурации."""
import pytest
from src.config import validate_args


def test_validate_args_success():
    """Тест успешной валидации (не должно быть исключений)."""
    class MockArgs:
        """Мок-объект аргументов командной строки."""
        max_depth = 2
        test_mode = False
        source = "url"

    validate_args(MockArgs())


def test_validate_args_fail_depth():
    """Тест некорректной глубины (ожидается исключение ValueError)."""
    class MockArgs:
        """Мок-объект аргументов командной строки."""
        max_depth = -2
        test_mode = False
        source = "url"

    with pytest.raises(ValueError):
        validate_args(MockArgs())
