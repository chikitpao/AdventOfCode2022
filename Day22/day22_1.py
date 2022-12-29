""" Advent of Code 2022, Day 22, Part 1
    Author: Chi-Kit Pao
"""


import os


def debug_output(message):
    print(message)
    pass


class Quiz:
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def __init__(self, input_file_name: str):
        self.instructions = None
        self.map = None
        # Use zero-based coordinates internally. Need one-based for answer.
        self.x = None  
        self.y = 0
        self.facing = Quiz.RIGHT
        self.__read_data(input_file_name)

    def run(self):
        for s in self.instructions:
            if s[0].isdigit():
                self.__walk(int(s))
            else:
                self.__turn(s)

    def __get_next_move(self):
        if self.facing == Quiz.RIGHT:
            def wrap_right():
                x = next(i for i, c in enumerate(self.map[self.y]) if c == '#' or c == '.')
                c = self.map[self.y][x]
                if c == '#':
                    return self.x, self.y
                elif c == '.':
                    return x, self.y
            if self.x == len(self.map[self.y]) - 1:
                return wrap_right()
            c =  self.map[self.y][self.x + 1]
            if c == '#':
                return self.x, self.y
            elif c == '.':
                return self.x + 1, self.y
            else:  # space
                return wrap_right()
        elif self.facing == Quiz.DOWN:
            def wrap_down():
                for y, map_line in enumerate(self.map):
                    if len(map_line) <= self.x:
                        continue
                    c = self.map[y][self.x]
                    if c == '#':
                        return self.x, self.y
                    elif c == '.':
                        return self.x, y
                    # else means c == ' ' -> continue
            if self.y == len(self.map) - 1 or self.x >= len(self.map[self.y + 1]):
                return wrap_down()
            c =  self.map[self.y + 1][self.x]
            if c == '#':
                return self.x, self.y
            elif c == '.':
                return self.x, self.y + 1
            else:  # space
                return wrap_down()
        elif self.facing == Quiz.LEFT:
            def wrap_left():
                for x in range(len(self.map[self.y]) - 1, -1, -1):
                    c = self.map[self.y][x]
                    if c == '#':
                        return self.x, self.y
                    elif c == '.':
                        return x, self.y
            if self.x == 0:
                return wrap_left()
            c =  self.map[self.y][self.x - 1]
            if c == '#':
                return self.x, self.y
            elif c == '.':
                return self.x - 1, self.y
            else:  # space
                return wrap_left()
        elif self.facing == Quiz.UP:
            def wrap_up():
                for y in range(len(self.map) - 1, -1, -1):
                    if len(self.map[y]) <= self.x:
                        continue
                    c = self.map[y][self.x]
                    if c == '#':
                        return self.x, self.y
                    elif c == '.':
                        return self.x, y
                    # else means c == ' ' -> continue
            if self.y == 0 or self.x >= len(self.map[self.y - 1]):
                return wrap_up()
            c =  self.map[self.y - 1][self.x]
            if c == '#':
                return self.x, self.y
            elif c == '.':
                return self.x, self.y - 1
            else:  # space
                return wrap_up()

    def __read_data(self, input_file_name: str):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', ''), f.readlines()))
            for line_no, line in enumerate(lines):
                if len(line) > 0 and line[0].isdigit():
                    self.instructions = line.replace('L', ' L ').replace('R', ' R ').split()
                    self.map = lines[:line_no - 1]
                    self.x = self.map[0].index('.')
                    break

    def __turn(self, direction: str):
        if direction == 'L':
            self.facing = Quiz.UP if self.facing == Quiz.RIGHT else self.facing - 1
        if direction == 'R':
            self.facing = Quiz.RIGHT if self.facing == Quiz.UP else self.facing + 1

    def __walk(self, steps: int):
        #debug_output(f'old: {self.x} {self.y} {self.facing} {steps}')
        for _ in range(steps):
            self.x, self.y = self.__get_next_move()
        #debug_output(f'new: {self.x} {self.y}')

def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1
    quiz = Quiz(file_names[file_names_index])
    quiz.run()

    print('# First question')
    print(f'The final password is {1000 * (quiz.y + 1) + 4 * (quiz.x + 1) + quiz.facing}.')

if __name__ == '__main__':
    main()