"""Точка входа для CLI инструмента трансляции."""
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET
from lark.exceptions import UnexpectedInput
from src.parser import config_parser
from src.transformer import ConfigTransformer


def format_xml(elem: ET.Element) -> str:
    """Форматирует XML с отступами для красивого вывода."""
    rough_string = ET.tostring(elem, "utf-8")
    parsed = xml.dom.minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="  ")


def main():
    """Читает stdin, парсит, сохраняет в XML файл."""
    if len(sys.argv) != 2:
        print("Использование: python -m src.main <output.xml>")
        sys.exit(1)

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

    except UnexpectedInput as e:
        print(f"Синтаксическая ошибка:\n{e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка трансляции:\n{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
