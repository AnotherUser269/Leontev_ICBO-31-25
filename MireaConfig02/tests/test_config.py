"""Тесты конфигурации."""
import pytest
from src.config import validate_args


def test_validate_args_success():
    """Тест успешной валидации."""
    class MockArgs:
        max_depth = 2
        test_mode = False
        source = "url"

    validate_args(MockArgs())  # Не должно быть исключений


def test_validate_args_fail_depth():
    """Тест некорректной глубины."""
    class MockArgs:
        max_depth = -2
        test_mode = False
        source = "url"

    with pytest.raises(ValueError):
        validate_args(MockArgs())
