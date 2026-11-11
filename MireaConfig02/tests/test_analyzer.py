"""Тесты анализатора графа."""
import json
from src.config import Config
from src.analyzer import build_transitive_graph, get_reverse_dependencies


def test_reverse_dependencies(tmp_path):
    """Тест поиска обратных зависимостей."""
    test_file = tmp_path / "data.json"
    test_file.write_text(json.dumps({
        "A": ["B"],
        "B": ["C"],
        "C": []
    }))
    
    config = Config(
        package="A", source=str(test_file), test_mode=True,
        version="latest", output="out.png", max_depth=-1,
        filter_substring=""
    )
    
    graph = build_transitive_graph(config)
    rev_deps = get_reverse_dependencies("C", graph)
    assert "B" in rev_deps
