"""Модуль анализа графа зависимостей."""
from dataclasses import replace
from typing import List
from src.config import Config
from src.graph import DependencyGraph
from src.fetcher import get_direct_dependencies

MAX_DEPTH_DEFAULT = -1


def build_transitive_graph(config: Config) -> DependencyGraph:
    """Построение транзитивного графа зависимостей с помощью DFS."""
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
    """Рекурсивный обход в глубину для построения графа."""
    if config.filter_substring and config.filter_substring in package:
        return

    if config.max_depth != MAX_DEPTH_DEFAULT:
        if current_depth > config.max_depth:
            return

    if package in visited:
        return

    visited.add(package)
    graph.graph.setdefault(package, [])

    current_config = replace(config, package=package)
    deps = get_direct_dependencies(current_config)

    for dep in deps:
        graph.add_edge(package, dep)
        _dfs_build(dep, current_depth + 1, config, graph, visited)


def get_reverse_dependencies(
    target_pkg: str, graph: DependencyGraph
) -> List[str]:
    """Поиск обратных зависимостей (кто зависит от target_pkg).

    Args:
        target_pkg: Целевой пакет.
        graph: Граф зависимостей.

    Returns:
        Список пакетов, зависящих от целевого.
    """
    reverse_deps = []
    for pkg, deps in graph.graph.items():
        if target_pkg in deps:
            reverse_deps.append(pkg)
    return reverse_deps
