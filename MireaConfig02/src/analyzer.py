"""Модуль анализа графа зависимостей."""
from src.config import Config
from src.graph import DependencyGraph
from src.fetcher import get_direct_dependencies

MAX_DEPTH_DEFAULT = -1


def build_transitive_graph(config: Config) -> DependencyGraph:
    """Построение транзитивного графа зависимостей с помощью DFS.

    Args:
        config: Конфигурация приложения.

    Returns:
        Построенный граф.
    """
    graph = DependencyGraph()
    visited = set()
    _dfs_build(config.package, 0, config, graph, visited)
    return graph


def _dfs_build(
    package: str,
    current_depth: int,
    config: Config,
    graph: DependencyGraph,
    visited: set
) -> None:
    """Рекурсивный обход в глубину для построения графа.

    Args:
        package: Текущий пакет.
        current_depth: Текущая глубина.
        config: Конфигурация.
        graph: Граф.
        visited: Множество посещенных пакетов.
    """
    # ИСПРАВЛЕНИЕ: проверяем, что строка фильтра не пустая
    if config.filter_substring and config.filter_substring in package:
        return
    
    if config.max_depth != MAX_DEPTH_DEFAULT:
        if current_depth > config.max_depth:
            return

    if package in visited:
        return

    visited.add(package)
    
    deps = get_direct_dependencies(
        Config(
            package=package,
            source=config.source,
            test_mode=config.test_mode,
            version=config.version,
            output=config.output,
            max_depth=config.max_depth,
            filter_substring=config.filter_substring
        )
    )

    for dep in deps:
        graph.add_edge(package, dep)
        _dfs_build(dep, current_depth + 1, config, graph, visited)
