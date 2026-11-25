"""Тесты для проверки парсера и трансформера учебного языка."""
import pytest
import xml.etree.ElementTree as ET
from lark.exceptions import UnexpectedInput
from src.parser import config_parser
from src.transformer import ConfigTransformer


def parse_and_transform(text: str) -> ET.Element:
    """Вспомогательная функция: парсит текст и возвращает XML-корень."""
    tree = config_parser.parse(text)
    return ConfigTransformer().transform(tree)


def test_basic_types():
    """Тест базовых типов: чисел и строк."""
    text = "42.5\n-3.14\n'hello world'"
    xml = parse_and_transform(text)
    
    assert len(xml) == 3
    assert xml[0].tag == "number"
    assert xml[0].get("value") == "42.5"
    assert xml[1].tag == "number"
    assert xml[1].get("value") == "-3.14"
    assert xml[2].tag == "string"
    assert xml[2].get("value") == "hello world"


def test_lists():
    """Тест массивов list(...)."""
    text = "list()\nlist(1.0)\nlist(1.0, 2.0, 'three')"
    xml = parse_and_transform(text)
    
    assert len(xml) == 3
    
    # Пустой список
    assert xml[0].tag == "list"
    assert len(xml[0]) == 0
    
    # Список с одним элементом
    assert xml[1].tag == "list"
    assert len(xml[1]) == 1
    assert xml[1][0].tag == "number"
    
    # Список с тремя элементами разных типов
    assert xml[2].tag == "list"
    assert len(xml[2]) == 3
    assert xml[2][0].tag == "number"
    assert xml[2][1].tag == "number"
    assert xml[2][2].tag == "string"


def test_dicts():
    """Тест словарей {...}."""
    text = "{}\n{ a = 1.0 }\n{ a = 1.0, b = 'str' }"
    xml = parse_and_transform(text)
    
    assert len(xml) == 3
    
    # Пустой словарь
    assert xml[0].tag == "dict"
    assert len(xml[0]) == 0
    
    # Словарь с одной парой
    assert xml[1].tag == "dict"
    assert len(xml[1]) == 1
    assert xml[1][0].tag == "entry"
    assert xml[1][0].get("key") == "a"
    
    # Словарь с двумя парами (разделены запятой)
    assert xml[2].tag == "dict"
    assert len(xml[2]) == 2
    assert xml[2][0].get("key") == "a"
    assert xml[2][1].get("key") == "b"


def test_nesting():
    """Тест вложенности списков и словарей."""
    text = "list({ a = 1.0 }, list(2.0, { b = 'str' }))"
    xml = parse_and_transform(text)
    
    root_list = xml[0]
    assert root_list.tag == "list"
    assert len(root_list) == 2
    
    # Первый элемент - словарь
    assert root_list[0].tag == "dict"
    assert root_list[0][0].get("key") == "a"
    
    # Второй элемент - вложенный список
    assert root_list[1].tag == "list"
    assert len(root_list[1]) == 2
    assert root_list[1][0].tag == "number"
    assert root_list[1][1].tag == "dict"


def test_constants():
    """Тест объявления и вычисления констант."""
    text = "def x = 10.0\ndef y = list(1.0)\nlist($[x], $[y])"
    xml = parse_and_transform(text)
    
    # Первые два элемента - объявления констант
    assert xml[0].tag == "constant"
    assert xml[0].get("name") == "x"
    assert xml[1].tag == "constant"
    assert xml[1].get("name") == "y"
    
    # Третий элемент - список с вычисленными константами
    assert xml[2].tag == "list"
    assert len(xml[2]) == 2
    
    # Значение константы x (10.0)
    assert xml[2][0].tag == "number"
    assert xml[2][0].get("value") == "10.0"
    
    # Значение константы y (список)
    assert xml[2][1].tag == "list"
    assert xml[2][1][0].tag == "number"


def test_comments():
    """Тест игнорирования однострочных и многострочных комментариев."""
    text = (
        "; Это однострочный комментарий\n"
        "<#\nЭто\nмногострочный\nкомментарий\n#>\n"
        "42.5\n"
        "; Еще комментарий"
    )
    xml = parse_and_transform(text)
    
    assert len(xml) == 1
    assert xml[0].tag == "number"
    assert xml[0].get("value") == "42.5"


def test_undefined_constant_error():
    """Тест выброса исключения при использовании неизвестной константы."""
    text = "list($[unknown])"
    with pytest.raises(ValueError, match="Неизвестная константа: unknown"):
        parse_and_transform(text)


def test_syntax_error():
    """Тест выброса синтаксической ошибки при неверном вводе."""
    # Имя переменной не может начинаться с заглавной буквы
    with pytest.raises(UnexpectedInput):
        config_parser.parse("def A = 1.0")
    
    # Отсутствует значение в словаре
    with pytest.raises(UnexpectedInput):
        config_parser.parse("{ a = }")


def test_real_config_example():
    """Интеграционный тест на основе примера ui_layout.conf."""
    text = """
<# 
Конфигурация UI окна
#>
def window_width = 1920.0

{
  window = {
    size = list($[window_width], 1080.0)
    title = 'My Application'
  }
}
    """
    xml = parse_and_transform(text)
    
    # Проверяем, что структура собралась без ошибок
    assert xml.find("constant").get("name") == "window_width"
    assert xml.find("dict").find("entry").get("key") == "window"
    
    window_dict = xml.find("dict").find("entry").find("dict")
    assert len(window_dict) == 2
    assert window_dict[0].get("key") == "size"
    assert window_dict[1].get("key") == "title"
