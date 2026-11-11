"""Тесты анализатора графа."""
import json
from src.config import Config
from src.analyzer import build_transitive_graph


def test_build_graph_cycle(tmp_path):
    """Тест обработки циклических зависимостей."""
    test_file = tmp_path / "data.json"
    test_file.write_text(json.dumps({
        "A": ["B"],
        "B": ["C"],
        "C": ["A"]
    }))
    
    config = Config(
        package="A", source=str(test_file), test_mode=True,
        version="latest", output="out.png", max_depth=-1,
        filter_substring=""
    )
    
    graph = build_transitive_graph(config)
    assert "A" in graph.graph
    assert "B" in graph.graph["A"]
    assert "C" in graph.graph["B"]
