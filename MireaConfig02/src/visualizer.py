"""Модуль визуализации графа зависимостей."""
import subprocess
from src.graph import DependencyGraph

PLANTUML_CMD = "plantuml"


def generate_plantuml_text(graph: DependencyGraph) -> str:
    """Генерация текста PlantUML.

    Args:
        graph: Граф зависимостей.

    Returns:
        Строка в формате PlantUML.
    """
    lines = ["@startuml"]
    for pkg, deps in graph.graph.items():
        if not deps:
            lines.append(f"[{pkg}]")
        for dep in deps:
            lines.append(f"[{pkg}] --> [{dep}]")
    lines.append("@enduml")
    return "\n".join(lines)


def save_visualization(graph: DependencyGraph, output_file: str) -> None:
    """Сохранение визуализации в PNG.

    Args:
        graph: Граф зависимостей.
        output_file: Имя выходного файла.
    """
    puml_text = generate_plantuml_text(graph)
    puml_file = output_file.replace(".png", ".puml")

    with open(puml_file, "w", encoding="utf-8") as file:
        file.write(puml_text)

    print(f"PlantUML text saved to {puml_file}")

    try:
        subprocess.run(
            [PLANTUML_CMD, "-tpng", puml_file],
            check=True,
            capture_output=True,
        )
        print(f"PNG image saved to {output_file}")
    except FileNotFoundError:
        print(
            "Error: 'plantuml' command not found. "
            "Please install PlantUML to generate PNG."
        )
    except subprocess.CalledProcessError as error:
        print(f"PlantUML error: {error.stderr.decode()}")
