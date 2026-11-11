"""Модуль для сбора информации о зависимостях."""
import json
import re
import urllib.request
from typing import List, Dict
from src.config import Config

PYPI_URL_TEMPLATE = "https://pypi.org/pypi/{package}/{version}/json"
PYPI_URL_LATEST = "https://pypi.org/pypi/{package}/json"
PKG_NAME_REGEX = r"^([a-zA-Z0-9\-_]+)"


def get_direct_dependencies(config: Config) -> List[str]:
    """Получение прямых зависимостей.

    Args:
        config: Конфигурация приложения.

    Returns:
        Список имен пакетов-зависимостей.
    """
    if config.test_mode:
        return _get_deps_from_test_file(config.source, config.package)
    return _get_deps_from_pypi(config.package, config.version)


def _get_deps_from_test_file(filepath: str, package: str) -> List[str]:
    """Чтение зависимостей из тестового файла.

    Args:
        filepath: Путь к файлу.
        package: Имя пакета.

    Returns:
        Список зависимостей.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        data: Dict[str, List[str]] = json.load(file)
    return data.get(package, [])


def _get_deps_from_pypi(package: str, version: str) -> List[str]:
    """Получение зависимостей из API PyPI.

    Args:
        package: Имя пакета.
        version: Версия пакета.

    Returns:
        Список прямых зависимостей.
    """
    if version == "latest":
        url = PYPI_URL_LATEST.format(package=package)
    else:
        url = PYPI_URL_TEMPLATE.format(package=package, version=version)

    # Добавляем User-Agent, чтобы PyPI не блокировал запросы
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'DependencyGraphVisualizer/1.0'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Failed to fetch data from PyPI: {e}")
        return []

    requires_dist = data.get("info", {}).get("requires_dist")
    if not requires_dist:
        return []

    return _parse_requires_dist(requires_dist)


def _parse_requires_dist(requires_dist: List[str]) -> List[str]:
    """Парсинг строк requires_dist.

    Args:
        requires_dist: Список строк с зависимостями.

    Returns:
        Очищенный список имен пакетов.
    """
    deps = []
    for req in requires_dist:
        match = re.match(PKG_NAME_REGEX, req)
        if match:
            deps.append(match.group(1).lower())
    return list(set(deps))
