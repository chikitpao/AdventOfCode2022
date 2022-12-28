""" Advent of Code 2022, Day 21, Part 2
    Author: Chi-Kit Pao
    REMARK: Requires sympy to run this program.
"""


import os
import sympy as sp


def debug_output(message):
    # print(message)
    pass


class Monkey:
    def __init__(self, name: str, expression: list[str]):
        self.name = name
        self.expression: str = None
        assert len(expression) == 1 or len(expression) == 3
        if len(expression) == 3:
            assert expression[1] in ['+', '-', '*', '/']
            if self.name != 'root':
                self.expression = f'({expression[0]}{expression[1]}{expression[2]})'
            else:
                self.expression = f'({expression[0]}-{expression[2]})'  # To solve lhs - rhs = 0
        elif len(expression) == 1:
            if self.name != 'humn':
                self.expression = expression[0]


class Quiz:
    def __init__(self, input_file_name: str):
        self.normal_monkeys: Monkey =  []
        self.root_monkey: Monkey = None
        self.human: Monkey = None
        self.__read_data(input_file_name)

    def run_calulation(self):
        while True:
            done_substitution: bool = False
            for monkey in self.normal_monkeys:
                if monkey.name in self.root_monkey.expression:
                    self.root_monkey.expression = self.root_monkey.expression.replace(monkey.name, monkey.expression)
                    done_substitution = True
            if not done_substitution:
                break

        print(f'Root\'s expression is {self.root_monkey.expression}.')
        humn = sp.symbols('humn')
        solution = sp.solve(sp.sympify(self.root_monkey.expression, evaluate=True), humn)[0]
        print(f'My number is {solution}.')

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
                if name == 'root':
                    self.root_monkey = monkey
                elif name == 'humn':
                    self.human = monkey
                else:
                    self.normal_monkeys.append(monkey)

def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1
    quiz = Quiz(file_names[file_names_index])

    print('# Second question')
    quiz.run_calulation()

if __name__ == '__main__':
    main()