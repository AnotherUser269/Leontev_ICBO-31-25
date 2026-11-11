"""Тесты модуля визуализации."""
from src.graph import DependencyGraph
from src.visualizer import generate_plantuml_text


def test_generate_plantuml() -> None:
    """Тест генерации PlantUML текста."""
    graph = DependencyGraph()
    graph.add_edge("A", "B")
    text = generate_plantuml_text(graph)
    assert "@startuml" in text
    assert "[A] --> [B]" in text
    assert "@enduml" in text
