"""Точка входа в приложение."""
import sys
from src.config import parse_args, print_config
from src.fetcher import get_direct_dependencies


def main() -> None:
    """Главная функция приложения."""
    try:
        config = parse_args()
        print_config(config)
        
        print("\nDirect dependencies:")
        deps = get_direct_dependencies(config)
        for dep in deps:
            print(f"- {dep}")
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
