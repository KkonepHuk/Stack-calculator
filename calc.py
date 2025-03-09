#!/usr/bin/env python3

from operator import add, sub, mul, truediv
import re

from compf import Compf
from roman_to_arabic_module import expression_to_arabic
from stack import Stack


class Calc(Compf):
    """
    Интерпретатор арифметических выражений вычисляет значения
    правильных арифметических формул, в которых в качестве
    операндов допустимы числа [0-9]+
    """

    SYMBOLS = re.compile("^[0-9]+$")

    def __init__(self):
        # Инициализация (конструктор) класса Compf
        super().__init__()
        # Создание стека чисел для работы стекового калькулятора
        self.r = Stack()

    # Приведение строчного выражения к списку
    # Позволяет использовать не только цифры, но и числа
    @staticmethod
    def _propagate(string):
        buffer = list()
        for char in string:
            if char.isdigit():
                buffer.append(char)
                continue

            if buffer:
                yield "".join(buffer)
                buffer.clear()
            yield char

    def propagate(self, string):
        return list(self._propagate("(" + string + ")"))

    # Интерпретация арифметического выражения
    def compile(self, string):
        self.data.clear()

        expression = expression_to_arabic(string)
        expression = expression.replace("**", "^")

        for c in self.propagate(expression):
            self.process_symbol(c)
        return self.r.top()

    # Обработка цифры
    def process_value(self, c):
        self.r.push(int(c))

    # Обработка символа операции
    def process_oper(self, c):
        second, first = self.r.pop(), self.r.pop()
        self.r.push(
            {"+": add, "-": sub, "*": mul, "/": truediv, "^": pow}[c](first, second)
        )


if __name__ == "__main__":
    c = Calc()
    while True:
        string = input("Арифметическое выражение: ")
        print(f"Результат его вычисления: {c.compile(string)}")
        print()
