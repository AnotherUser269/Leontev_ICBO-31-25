"""Модуль настройки парсера для учебного конфигурационного языка."""
import os
from lark import Lark

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "grammar.lark")

with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
    GRAMMAR = f.read()

config_parser = Lark(GRAMMAR, parser="earley", propagate_positions=True)
