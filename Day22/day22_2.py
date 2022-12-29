""" Advent of Code 2022, Day 22, Part 2
    Author: Chi-Kit Pao
"""


import os


def debug_output(message):
    # print(message)
    pass

class Surface:
    def __init__(self, index, left, top, right, bottom):
        self.index = index
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.transitions = []

    def get_next_tile(self, x, y, facing):
        if facing == Quiz.RIGHT:
            if x == self.right:
                return self.transitions[facing](x, y)
            return (x + 1, y, facing, self.index)
        elif facing == Quiz.DOWN:
            if y == self.bottom:
                return self.transitions[facing](x, y)
            return (x, y + 1, facing, self.index)
        elif facing == Quiz.LEFT:
            if x == self.left:
                return self.transitions[facing](x, y)
            return (x - 1, y, facing, self.index)
        elif facing == Quiz.UP:
            if y == self.top:
                return self.transitions[facing](x, y)
            return (x, y - 1, facing, self.index)


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
        self.surface = 1  # surface on cube
        self.surface_data = {}
        self.__read_data(input_file_name)
        self.__init_cube(input_file_name)

    def run(self):
        for s in self.instructions:
            if s[0].isdigit():
                self.__walk(int(s))
            else:
                self.__turn(s)

    def __get_next_move(self):
        current_surface = self.surface_data[self.surface]
        next_tile = current_surface.get_next_tile(self.x, self.y, self.facing)
        debug_output(f'self {self.x}, {self.y}, {self.facing}, {self.surface}')
        debug_output(f'next_tile: {next_tile}')
        if self.map[next_tile[1]][next_tile[0]] == '#':
            return self.x, self.y, self.facing, self.surface
        elif self.map[next_tile[1]][next_tile[0]] == '.':
            return next_tile[0], next_tile[1], next_tile[2], next_tile[3]
        else:
                assert False, f'Invalid tile: \'{self.map[next_tile[1]][next_tile[0]]}\''
    
    def __init_cube(self, input_file_name: str):
        max_width = max(list(len(l) for l in self.map))
        height = len(self.map)
        debug_output(f'height: {height}, max width = {max_width}')
        assert input_file_name == 'test.txt' or input_file_name == 'input1.txt'
        if input_file_name == 'test.txt':
            cube_length = height // 3
            assert cube_length == max_width // 4
            self.surface_data[1] = Surface(1, 2 * cube_length, 0, 3 * cube_length - 1, cube_length - 1)
            self.surface_data[1].transitions = [\
                lambda x, y: (self.surface_data[6].right, self.surface_data[6].bottom - (y - self.surface_data[1].top), Quiz.LEFT, 6), \
                lambda x, y: (x, y + 1, Quiz.DOWN, 4), \
                lambda x, y: (self.surface_data[3].left + (y - self.surface_data[1].top) , self.surface_data[3].top, Quiz.DOWN, 3), \
                lambda x, y: (self.surface_data[2].right - (x - self.surface_data[1].left), self.surface_data[2].top, Quiz.DOWN, 2) \
                ]
            self.surface_data[2] = Surface(2, 0, cube_length, cube_length -1, 2 * cube_length - 1)
            self.surface_data[2].transitions = [\
                lambda x, y: (x + 1, y, Quiz.RIGHT, 3), \
                lambda x, y: (self.surface_data[5].right - (x - self.surface_data[2].left), self.surface_data[5].bottom, Quiz.UP, 5), \
                lambda x, y: (self.surface_data[6].right - (y - self.surface_data[2].top), self.surface_data[6].bottom, Quiz.UP, 6), \
                lambda x, y: (self.surface_data[1].right - (x - self.surface_data[2].left), self.surface_data[1].top, Quiz.DOWN, 1) \
                ]            
            self.surface_data[3] = Surface(3, cube_length, cube_length, 2 * cube_length - 1, 2 * cube_length - 1)
            self.surface_data[3].transitions = [\
                lambda x, y: (x + 1, y, Quiz.RIGHT, 4), \
                lambda x, y: (self.surface_data[5].left, self.surface_data[5].bottom - (x - self.surface_data[3].left), Quiz.RIGHT, 5), \
                lambda x, y: (x - 1, y, Quiz.LEFT, 2), \
                lambda x, y: (self.surface_data[1].left, self.surface_data[1].top + (x - self.surface_data[3].left), Quiz.RIGHT, 1) \
                ]
            self.surface_data[4] = Surface(4, 2 * cube_length, cube_length, 3 * cube_length - 1, 2 * cube_length - 1)
            self.surface_data[4].transitions = [\
                lambda x, y: (self.surface_data[6].right - (y - self.surface_data[4].top), self.surface_data[6].top, Quiz.DOWN, 6), \
                lambda x, y: (x, y + 1, Quiz.UP, 5), \
                lambda x, y: (x - 1, y, Quiz.LEFT, 3), \
                lambda x, y: (x, y - 1, Quiz.UP, 1) \
                ]
            self.surface_data[5] = Surface(5, 2 * cube_length, 2 * cube_length, 3 * cube_length - 1, 3 * cube_length - 1)
            self.surface_data[5].transitions = [\
                lambda x, y: (x + 1, y, Quiz.RIGHT, 6), \
                lambda x, y: (self.surface_data[2].right - (x - self.surface_data[5].left), self.surface_data[2].bottom, Quiz.UP, 2), \
                lambda x, y: (self.surface_data[3].right - (y - self.surface_data[5].top), self.surface_data[3].bottom, Quiz.UP, 3), \
                lambda x, y: (x, y - 1, Quiz.UP, 4) \
                ]
            self.surface_data[6] = Surface(6, 3 * cube_length, 2 * cube_length, 4 * cube_length - 1, 3 * cube_length - 1)
            self.surface_data[6].transitions = [\
                lambda x, y: (self.surface_data[1].right, self.surface_data[1].bottom - (y - self.surface_data[6].top), Quiz.LEFT, 1), \
                lambda x, y: (self.surface_data[2].left, self.surface_data[2].bottom - (x - self.surface_data[6].left), Quiz.RIGHT, 2), \
                lambda x, y: (x - 1, y, Quiz.LEFT, 5), \
                lambda x, y: (self.surface_data[4].right, self.surface_data[4].bottom - (x - self.surface_data[6].left), Quiz.LEFT, 4) \
                ]                   
        else:
            cube_length = height // 4
            assert cube_length == max_width // 3
            self.surface_data[1] = Surface(1, cube_length, 0, 2 * cube_length - 1, cube_length - 1)
            self.surface_data[1].transitions = [\
                lambda x, y: (x + 1, y, Quiz.RIGHT, 2), \
                lambda x, y: (x, y + 1, Quiz.DOWN, 3), \
                lambda x, y: (self.surface_data[4].left, self.surface_data[4].bottom - (y - self.surface_data[1].top), Quiz.RIGHT, 4), \
                lambda x, y: (self.surface_data[6].left, self.surface_data[6].top + (x - self.surface_data[1].left), Quiz.RIGHT, 6) \
                ]
            self.surface_data[2] = Surface(2, 2 * cube_length, 0, 3 * cube_length - 1, cube_length - 1)
            self.surface_data[2].transitions = [\
                lambda x, y: (self.surface_data[5].right, self.surface_data[5].bottom - (y - self.surface_data[2].top), Quiz.LEFT, 5), \
                lambda x, y: (self.surface_data[3].right, self.surface_data[3].top + (x - self.surface_data[2].left), Quiz.LEFT, 3), \
                lambda x, y: (x - 1, y, Quiz.LEFT, 1), \
                lambda x, y: (self.surface_data[6].left + (x - self.surface_data[2].left), self.surface_data[6].bottom, Quiz.UP, 6) \
                ]
            self.surface_data[3] = Surface(3, cube_length, cube_length, 2 * cube_length - 1, 2 * cube_length - 1)
            self.surface_data[3].transitions = [\
                lambda x, y: (self.surface_data[2].left + (y - self.surface_data[3].top), self.surface_data[2].bottom, Quiz.UP, 2), \
                lambda x, y: (x, y + 1, Quiz.DOWN, 5), \
                lambda x, y: (self.surface_data[4].left + (y - self.surface_data[3].top), self.surface_data[4].top, Quiz.DOWN, 4), \
                lambda x, y: (x, y - 1, Quiz.UP, 1) \
                ]
            self.surface_data[4] = Surface(4, 0, 2 * cube_length, cube_length - 1, 3 * cube_length - 1)
            self.surface_data[4].transitions = [\
                lambda x, y: (x + 1, y, Quiz.RIGHT, 5), \
                lambda x, y: (x, y + 1, Quiz.DOWN, 6), \
                lambda x, y: (self.surface_data[1].left, self.surface_data[1].bottom - (y - self.surface_data[4].top), Quiz.RIGHT, 1), \
                lambda x, y: (self.surface_data[3].left, self.surface_data[3].top + (x - self.surface_data[4].left), Quiz.RIGHT, 3) \
                ]
            self.surface_data[5] = Surface(5, cube_length, 2 * cube_length, 2 * cube_length - 1, 3 * cube_length - 1)
            self.surface_data[5].transitions = [\
                lambda x, y: (self.surface_data[2].right, self.surface_data[2].bottom - (y - self.surface_data[5].top), Quiz.LEFT, 2), \
                lambda x, y: (self.surface_data[6].right, self.surface_data[6].top + (x - self.surface_data[5].left), Quiz.LEFT, 6), \
                lambda x, y: (x - 1, y, Quiz.LEFT, 4), \
                lambda x, y: (x, y - 1, Quiz.UP, 3) \
                ]
            self.surface_data[6] = Surface(6, 0, 3 * cube_length, cube_length - 1, 4 * cube_length - 1)
            self.surface_data[6].transitions = [\
                lambda x, y: (self.surface_data[5].left + (y - self.surface_data[6].top), self.surface_data[5].bottom, Quiz.UP, 5), \
                lambda x, y: (self.surface_data[2].left + (x - self.surface_data[6].left), self.surface_data[2].top, Quiz.DOWN, 2), \
                lambda x, y: (self.surface_data[1].left + (y - self.surface_data[6].top), self.surface_data[1].top, Quiz.DOWN, 1), \
                lambda x, y: (x, y - 1, Quiz.UP, 4) \
                ]

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
        debug_output(f'old: {self.x} {self.y} {self.facing} {steps}')
        for _ in range(steps):
            self.x, self.y, self.facing, self.surface = self.__get_next_move()
        debug_output(f'new: {self.x} {self.y}')

def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1
    quiz = Quiz(file_names[file_names_index])
    quiz.run()

    print('# Second question')
    print(f'The final password is {1000 * (quiz.y + 1) + 4 * (quiz.x + 1) + quiz.facing}.')


if __name__ == '__main__':
    main()
