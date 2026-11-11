"""Тесты модуля сбора данных."""
import json
from src.fetcher import _get_deps_from_test_file, _parse_requires_dist


def test_get_deps_from_test_file(tmp_path):
    """Тест чтения из тестового файла."""
    test_file = tmp_path / "data.json"
    test_file.write_text(json.dumps({"A": ["B", "C"]}))
    
    deps = _get_deps_from_test_file(str(test_file), "A")
    assert deps == ["B", "C"]


def test_parse_requires_dist():
    """Тест парсинга requires_dist."""
    reqs = ["requests (>=2.0)", "numpy"]
    deps = _parse_requires_dist(reqs)
    assert "requests" in deps
    assert "numpy" in deps
