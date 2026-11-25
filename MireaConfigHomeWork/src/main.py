"""Точка входа для CLI инструмента трансляции."""
import sys
import xml.dom.minidom
import xml.etree.ElementTree as etree
from lark.exceptions import UnexpectedInput
from src.parser import config_parser
from src.transformer import ConfigTransformer

_EXPECTED_ARGV_LEN = 2
_EXIT_SUCCESS = 0
_EXIT_ERROR = 1
_XML_INDENT = "  "


def format_xml(elem: etree.Element) -> str:
    """Форматирует XML с отступами для красивого вывода."""
    rough_string = etree.tostring(elem, "utf-8")
    parsed = xml.dom.minidom.parseString(rough_string)
    return parsed.toprettyxml(indent=_XML_INDENT)


def main():
    """Читает stdin, парсит, сохраняет в XML файл."""
    if len(sys.argv) != _EXPECTED_ARGV_LEN:
        print("Использование: python -m src.main <output.xml>")
        sys.exit(_EXIT_ERROR)

    output_file = sys.argv[1]
    input_text = sys.stdin.read()

    try:
        tree = config_parser.parse(input_text)
        transformer = ConfigTransformer()
        xml_root = transformer.transform(tree)

        formatted_xml = format_xml(xml_root)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_xml)

        print(f"Успешно скомпилировано в {output_file}")
        sys.exit(_EXIT_SUCCESS)

    except UnexpectedInput as e:
        print(f"Синтаксическая ошибка:\n{e}", file=sys.stderr)
        sys.exit(_EXIT_ERROR)
    except ValueError as e:
        print(f"Ошибка трансляции:\n{e}", file=sys.stderr)
        sys.exit(_EXIT_ERROR)


if __name__ == "__main__":
    main()
