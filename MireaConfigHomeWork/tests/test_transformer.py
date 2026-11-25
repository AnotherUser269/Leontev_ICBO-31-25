"""Тесты для проверки парсера и трансформера учебного языка."""
import pytest
import xml.etree.ElementTree as etree
from lark.exceptions import UnexpectedInput
from src.parser import config_parser
from src.transformer import ConfigTransformer

_LEN_EMPTY = 0
_LEN_SINGLE = 1
_LEN_PAIR = 2
_LEN_TRIPLE = 3


def parse_and_transform(text: str) -> etree.Element:
    """Парсит текст и возвращает корневой XML-элемент."""
    tree = config_parser.parse(text)
    return ConfigTransformer().transform(tree)


def test_number():
    """Тест числового литерала."""
    xml = parse_and_transform("42.5")
    assert xml[0].tag == "number"
    assert xml[0].get("value") == "42.5"


def test_negative_number():
    """Тест отрицательного числа."""
    xml = parse_and_transform("-3.14")
    assert xml[0].tag == "number"
    assert xml[0].get("value") == "-3.14"


def test_string():
    """Тест строкового литерала."""
    xml = parse_and_transform("'hello world'")
    assert xml[0].tag == "string"
    assert xml[0].get("value") == "hello world"


def test_empty_list():
    """Тест пустого массива."""
    xml = parse_and_transform("list()")
    assert xml[0].tag == "list"
    assert len(xml[0]) == _LEN_EMPTY


def test_list_with_one_element():
    """Тест массива с одним элементом."""
    xml = parse_and_transform("list(1.0)")
    assert xml[0].tag == "list"
    assert len(xml[0]) == _LEN_SINGLE
    assert xml[0][0].tag == "number"


def test_list_with_three_elements():
    """Тест массива из трёх элементов разных типов."""
    xml = parse_and_transform("list(1.0, 2.0, 'three')")
    assert xml[0].tag == "list"
    assert len(xml[0]) == _LEN_TRIPLE
    assert xml[0][2].tag == "string"


def test_empty_dict():
    """Тест пустого словаря."""
    xml = parse_and_transform("{}")
    assert xml[0].tag == "dict"
    assert len(xml[0]) == _LEN_EMPTY


def test_dict_with_one_pair():
    """Тест словаря с одной парой."""
    xml = parse_and_transform("{ a = 1.0 }")
    assert xml[0].tag == "dict"
    assert len(xml[0]) == _LEN_SINGLE
    assert xml[0][0].get("key") == "a"


def test_dict_with_two_pairs():
    """Тест словаря с двумя парами через запятую."""
    xml = parse_and_transform("{ a = 1.0, b = 'str' }")
    assert xml[0].tag == "dict"
    assert len(xml[0]) == _LEN_PAIR
    assert xml[0][1].get("key") == "b"


def test_nested_list_in_dict():
    """Тест списка внутри словаря."""
    xml = parse_and_transform("{ a = list(1.0) }")
    assert xml[0][0][0].tag == "list"


def test_nested_dict_in_list():
    """Тест словаря внутри списка."""
    xml = parse_and_transform("list({ a = 1.0 })")
    assert xml[0][0].tag == "dict"


def test_deep_nesting():
    """Тест глубокой вложенности."""
    xml = parse_and_transform("list({ a = list(1.0) })")
    assert xml[0][0][0][0].tag == "number"


def test_constant_declaration():
    """Тест объявления константы."""
    xml = parse_and_transform("def x = 10.0")
    assert xml[0].tag == "constant"
    assert xml[0].get("name") == "x"


def test_constant_evaluation():
    """Тест вычисления константы через $[name]."""
    xml = parse_and_transform("def x = 10.0\nlist($[x])")
    assert xml[0].tag == "constant"
    assert xml[1][0].get("value") == "10.0"


def test_constant_inside_dict():
    """Тест константы внутри словаря."""
    text = "def n = 5.0\n{ a = $[n] }"
    xml = parse_and_transform(text)
    assert xml[1][0][0].get("value") == "5.0"


def test_single_line_comment_ignored():
    """Тест игнорирования однострочного комментария."""
    xml = parse_and_transform("; comment\n42.5")
    assert xml[0].tag == "number"


def test_multiline_comment_ignored():
    """Тест игнорирования многострочного комментария."""
    xml = parse_and_transform("<#\nmulti\nline\n#>\n42.5")
    assert xml[0].tag == "number"


def test_undefined_constant_error():
    """Тест ошибки при неизвестной константе."""
    text = "list($[unknown])"
    with pytest.raises(ValueError, match="Неизвестная константа: unknown"):
        parse_and_transform(text)


def test_uppercase_name_syntax_error():
    """Тест синтаксической ошибки на заглавную букву в имени."""
    with pytest.raises(UnexpectedInput):
        config_parser.parse("def A = 1.0")


def test_missing_value_syntax_error():
    """Тест синтаксической ошибки при отсутствии значения."""
    with pytest.raises(UnexpectedInput):
        config_parser.parse("{ a = }")
