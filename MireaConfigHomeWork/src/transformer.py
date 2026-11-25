"""Модуль трансформации AST в XML и вычисления констант."""
import xml.etree.ElementTree as ET
from lark import Transformer, v_args


class ConfigTransformer(Transformer):
    """Преобразует дерево разбора Lark в XML структуру."""

    def __init__(self):
        super().__init__()
        self.constants = {}
        self.root = ET.Element("config")

    @v_args(inline=True)
    def number(self, token):
        """Обрабатывает числовые литералы."""
        return ET.Element("number", value=str(token))

    @v_args(inline=True)
    def string(self, token):
        """Обрабатывает строковые литералы."""
        val = str(token).strip("'")
        return ET.Element("string", value=val)

    def list_expr(self, items):
        """Обрабатывает массивы list(...)."""
        list_elem = ET.Element("list")
        for item in items:
            list_elem.append(item)
        return list_elem

    def pair(self, items):
        """Обрабатывает пару ключ-значение в словаре."""
        key = str(items[0])  # items[0] теперь чистый Token, str даст имя
        val = items[1]
        entry = ET.Element("entry", key=key)
        entry.append(val)
        return entry

    def dict(self, items):
        """Обрабатывает словари {...}."""
        dict_elem = ET.Element("dict")
        for item in items:
            dict_elem.append(item)
        return dict_elem

    @v_args(inline=True)
    def const_eval(self, name_token):
        """Вычисляет константу на этапе трансляции."""
        name = str(name_token)
        if name not in self.constants:
            raise ValueError(f"Неизвестная константа: {name}")

        return ET.fromstring(ET.tostring(self.constants[name]))

    @v_args(inline=True)
    def const_decl(self, name_token, expr_elem):
        """Объявляет константу def name = value."""
        name = str(name_token)
        self.constants[name] = expr_elem
        const_elem = ET.Element("constant", name=name)
        const_elem.append(expr_elem)
        self.root.append(const_elem)
        return const_elem

    def start(self, items):
        """Корневой узел. Собирает все выражения."""
        for item in items:
            if item.tag != "constant":
                self.root.append(item)
        return self.root
