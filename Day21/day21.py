""" Advent of Code 2022, Day 21
    Author: Chi-Kit Pao
"""


import os


def debug_output(message):
    # print(message)
    pass


class Monkey:
    def __init__(self, name: str, expression: list[str]):
        self.name = name
        self.operation: str = None
        self.var1: str = None
        self.var2: str = None
        self.op1: int = None
        self.op2: int = None
        self.number: int = None
        assert len(expression) == 1 or len(expression) == 3
        if len(expression) == 3:
            self.operation = expression[1]
            assert self.operation in ['+', '-', '*', '/']
            self.var1 = expression[0]
            self.var2 = expression[2]
        elif len(expression) == 1:
            self.number = int(expression[0])
    
    def do_operation(self):
        if self.operation == '+':
            self.number = self.op1 + self.op2
        elif self.operation == '-':
            self.number = self.op1 - self.op2
        elif self.operation == '*':
            self.number = self.op1 * self.op2
        elif self.operation == '/':
            self.number = self.op1 // self.op2


class Quiz:
    def __init__(self, input_file_name: str):
        self.monkeys = {}  # name -> Monkey
        self.calculating_monkeys: list[Monkey] = []
        self.__read_data(input_file_name)

    def run_calulation(self):
        while len(self.calculating_monkeys) > 0:
            done_substitution: bool = False
            for monkey in self.calculating_monkeys:
                if monkey.op1 is None and self.monkeys[monkey.var1].number is not None:
                    monkey.op1 = self.monkeys[monkey.var1].number
                    done_substitution = True
                if monkey.op2 is None and self.monkeys[monkey.var2].number is not None:
                    monkey.op2 = self.monkeys[monkey.var2].number
                    done_substitution = True
                if monkey.op1 is not None and monkey.op2 is not None:
                    monkey.do_operation()
                    self.calculating_monkeys.remove(monkey)
            if not done_substitution:
                pass

        root_number = self.monkeys['root'].number
        print(f'Root yells {root_number}!')

    def __read_data(self, input_file_name: str):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            for line in lines:
                # Line examples:
                # 'root: pppw + sjmn'
                # 'dbpl: 5'
                tokens = line.split()
                if len(tokens) == 0:
                    continue
                name = tokens[0].replace(':', '')
                monkey = Monkey(name, tokens[1:])
                self.monkeys[name] = monkey
                if monkey.operation is not None:
                    self.calculating_monkeys.append(monkey)


def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1
    quiz = Quiz(file_names[file_names_index])

    print('# First question')
    quiz.run_calulation()

if __name__ == '__main__':
    main()