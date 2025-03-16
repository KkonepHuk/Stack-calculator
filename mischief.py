#!/usr/bin/env python3


from compf import Compf
from stack import Stack


class Group:
    """
    Группа есть часть выражения с общим оператором
    В аттрибуте 'tokens' содержатся аргументы
    В аттрибуте 'op' содержится общий для аргументов оператор
    """

    def __init__(self, op: str, tokens: list):
        self.op = op
        self.tokens = tokens

    # Этот метод позволяет проверять наличие аргумента в группе
    def __iter__(self):
        for token in self.tokens:
            yield token

    # Сравнение с группой производится по ее оператору
    def __eq__(self, other):
        return self.op == other

    # Следующие методы копируют поведение списков
    def append(self, token):
        self.tokens.append(token)

    def extend(self, tokens):
        for token in tokens:
            self.append(token)

    def sort(self):
        self.tokens.sort()

    # Следующие методы недоступны пользователю, воздержимся от проверок
    def insert(self, index: int, token):
        self.tokens.insert(index, token)

    def pop(self, index: int):
        self.tokens.pop(index)


class Mischief(Compf):
    def __init__(self):
        super().__init__()
        # Стек для обработки групп. Принцип похож на работу калькулятора
        self.g = Stack()

    def compile(self, string):
        # Сначала компилируем выражение. Здесь никаких изменений нет
        super().compile(string)

        for token in self.data:
            # Аргументы просто кладем на стек
            if token not in "+-*/":
                self.g.push(token)
                continue
            second, first = self.g.pop(), self.g.pop()

            # Некоммутативные операции всегда берем в группу
            if token not in "+*":
                self.g.push(Group(token, [first, second]))
                continue

            # Далее сравниваем оператор группы с текущим оператором

            # Принадлежность аргументов к группам (isinstance()) не проверяем,
            # ведь если среди аргументов каким-то образом оказались операторы,
            # то программа уже давным давно сломалась

            # Если оператор группы и текущий оператор равны...
            if first == token:
                # Применяем правило ассоциативности
                if first == second:
                    # Если второй аргумент есть группа, то объединяем ее с первой
                    first.extend(second)
                else:
                    # В противном случае добавляем аргумент в первую группу
                    first.append(second)
                # В отличие от калькулятора, здесь мы возвращаем группу на стек
                self.g.push(first)
            elif second == token:
                # Те же операции для случая, когда группой является только второй аргумент

                # Совпадение операторов мы уже проверяли
                # Здесь аргумент однозначно добавляется в начало группы
                second.insert(0, first)
                self.g.push(second)
            else:
                self.g.push(Group(token, [first, second]))

        # Компонуем преобразования
        generator = (f for f in self._flatten(self._descend(self.g.pop())))

        for i in range(len(self.data)):
            # Заменяем только аргументы, на аргументы в отсортированном порядке
            if self.data[i] in "+-*/":
                continue
            self.data[i] = next(generator)

        return " ".join(self.data)

    # Сортировка групп
    def _descend(self, tokens):
        # Так как сортировать группы нельзя, сперва уберем их
        # За ключи возьмем индексы групп, а за значения - сами группы
        storage = dict()

        for i, token in enumerate(tokens):
            if not isinstance(token, Group):
                continue
            storage[i] = token

        # Будем удалять индексы по убывающей, чтобы не влиять на другие индексы
        for index in sorted(storage, reverse=True):
            tokens.pop(index)

        # Сортируем только аргументы коммутативных операций
        if tokens == "+" or tokens == "*":
            tokens.sort()

        # Восстанавливаем группы, предварительно отсортировав их
        for index, group in storage.items():
            tokens.insert(index, self._descend(group))
        return tokens

    # Распаковка групп
    def _flatten(self, tokens):
        result = list()

        for token in tokens:
            if not isinstance(token, Group):
                result.append(token)
            else:
                result.extend(self._flatten(token))
        return result


if __name__ == "__main__":
    m = Mischief()
    while True:
        string = input("Арифметическая  формула: ")
        result = m.compile(string)
        print(f"Результат её компиляции: {result}")
        print()
