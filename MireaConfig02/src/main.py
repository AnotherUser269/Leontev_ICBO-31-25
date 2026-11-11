"""Точка входа в приложение."""
import sys
from src.config import parse_args, print_config


def main() -> None:
    """Главная функция приложения."""
    try:
        config = parse_args()
        print_config(config)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
