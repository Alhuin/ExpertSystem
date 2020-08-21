from enum import Enum


class Operators(Enum):
    AND = '+'
    OR = '|'
    XOR = '^'


class AND:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        if self.a == 'Undetermined' and self.b == 'Undetermined':
            self.result = True
        else:
            self.result = self.a and self.b

    def run(self):
        # print(f"{self.a} AND {self.b} = {self.result}")
        return self.result

    def print(self):
        print(self.result)


class OR:
    def __init__(self, a, b):
        self.a = a if a != ['Undetermined', False] else [False, False]
        self.b = b if b != ['Undetermined', False] else [False, False]
        self.result = self.a[0] or self.b[0]

    def run(self):
        # print(f"{self.a} OR {self.b} = {self.result}")
        return self.result

    def print(self):
        print(self.result)


class XOR:
    def __init__(self, a, b):
        self.a = a if a != ['Undetermined', False] else [False, False]
        self.b = b if b != ['Undetermined', False] else [False, False]

        if (self.a == [False, False] and self.b == [True, True]) or (self.a == [True, True] and self.b == [False, False]):
            self.result = True
        else:
            self.result = self.a[0] != self.b[0]

    def run(self):
        # print(f"{self.a} XOR {self.b} = {self.result}")
        return self.result

    def print(self):
        print(self.result)
