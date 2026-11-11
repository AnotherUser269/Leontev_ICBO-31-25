"""Точка входа в приложение."""
import sys
from src.config import parse_args, print_config
from src.analyzer import build_transitive_graph


def main() -> None:
    """Главная функция приложения."""
    try:
        config = parse_args()
        print_config(config)
        
        print("\nBuilding dependency graph...")
        graph = build_transitive_graph(config)
        
        print("\nGraph edges:")
        for pkg, deps in graph.graph.items():
            for dep in deps:
                print(f"{pkg} -> {dep}")
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
