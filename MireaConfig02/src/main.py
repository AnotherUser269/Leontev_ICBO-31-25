"""Точка входа в приложение."""
import sys
from src.config import parse_args, print_config
from src.analyzer import build_transitive_graph, get_reverse_dependencies
from src.visualizer import save_visualization


def main() -> None:
    """Главная функция приложения."""
    try:
        config = parse_args()
        print_config(config)

        print("\nBuilding dependency graph...")
        graph = build_transitive_graph(config)

        if config.reverse:
            print(f"\nReverse dependencies for {config.package}:")
            for dep in get_reverse_dependencies(config.package, graph):
                print(f"- {dep}")
        else:
            print("\nGraph edges:")
            if not graph.graph:
                print("(empty)")
            for pkg, deps in graph.graph.items():
                if not deps:
                    print(f"{pkg} -> (no dependencies)")
                for dep in deps:
                    print(f"{pkg} -> {dep}")

            print("\nVisualizing graph...")
            save_visualization(graph, config.output)

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
