"""Модуль конфигурации CLI-приложения."""
import argparse
from dataclasses import dataclass

MAX_DEPTH_DEFAULT = -1


@dataclass
class Config:
    """Класс для хранения конфигурации."""
    package: str
    source: str
    test_mode: bool
    version: str
    output: str
    max_depth: int
    filter_substring: str
    reverse: bool


def _create_parser() -> argparse.ArgumentParser:
    """Создание и настройка парсера аргументов.

    Returns:
        Инициализированный парсер.
    """
    parser = argparse.ArgumentParser(description="Dependency Visualizer")
    
    parser.add_argument("--package", required=True, help="Package name")
    parser.add_argument("--source", required=True, help="Repo URL or path")
    parser.add_argument("--test-mode", action="store_true", help="Test mode")
    parser.add_argument("--version", default="latest", help="Version")
    parser.add_argument("--output", default="graph.png", help="Output file")
    parser.add_argument("--filter", default="", help="Filter substring")
    
    parser.add_argument(
        "--max-depth", type=int, default=MAX_DEPTH_DEFAULT,
        help="Maximum analysis depth"
    )
    parser.add_argument(
        "--reverse", action="store_true",
        help="Show reverse dependencies"
    )
    
    return parser


def _create_config(args: argparse.Namespace) -> Config:
    """Создание объекта конфигурации из аргументов.

    Args:
        args: Аргументы командной строки.

    Returns:
        Объект конфигурации.
    """
    return Config(
        package=args.package,
        source=args.source,
        test_mode=args.test_mode,
        version=args.version,
        output=args.output,
        max_depth=args.max_depth,
        filter_substring=args.filter,
        reverse=args.reverse
    )


def parse_args() -> Config:
    """Парсинг аргументов командной строки.

    Returns:
        Config: Объект с настройками.
    """
    parser = _create_parser()
    args = parser.parse_args()
    
    validate_args(args)
    
    return _create_config(args)


def validate_args(args: argparse.Namespace) -> None:
    """Валидация аргументов.

    Args:
        args: Аргументы командной строки.

    Raises:
        ValueError: Если аргументы некорректны.
    """
    if args.max_depth < MAX_DEPTH_DEFAULT:
        raise ValueError("Max depth must be >= -1")

    if not args.test_mode and args.source == "":
        raise ValueError("Source cannot be empty in normal mode")


def print_config(config: Config) -> None:
    """Вывод конфигурации в формате ключ-значение.

    Args:
        config: Объект конфигурации.
    """
    print(f"package={config.package}")
    print(f"source={config.source}")
    print(f"test_mode={config.test_mode}")
    print(f"version={config.version}")
    print(f"output={config.output}")
    print(f"max_depth={config.max_depth}")
    print(f"filter={config.filter_substring}")
    print(f"reverse={config.reverse}")
