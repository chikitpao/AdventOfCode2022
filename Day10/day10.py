""" Advent of Code 2022, Day 10
    Author: Chi-Kit Pao
"""

import os


class Screen:
    def __init__(self, input_file_name: str):
        self.register_x = 1
        self.cycle = 1
        self.sum = 0  # sum of signal strengths
        self.watch_list = [20, 60, 100, 140, 180, 220]
        self.screen_width = 40
        self.output = [ [] for _ in range(7) ]

        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            self.lines = list(map(lambda s: s.replace('\n', ''), f.readlines()))
    
    def execute_instructions(self):
        for line in self.lines:
            instruction = line.split()
            if instruction[0] == 'noop':
                self.handle_cycle()
                self.cycle += 1
            elif instruction[0] == 'addx':
                self.handle_cycle()
                self.cycle += 1
                self.handle_cycle()
                self.cycle += 1
                self.register_x += int(instruction[1])
    
    def handle_cycle(self):
        if self.cycle in self.watch_list:
            self.sum += self.cycle * self.register_x
        sprite_position = [self.register_x - 1, self.register_x, self.register_x + 1]
        row = (self.cycle - 1) // self.screen_width
        col = (self.cycle - 1) % self.screen_width
        char = '#' if col in sprite_position else '.'
        self.output[row].append(char)


def main():
    screen = Screen('input1.txt')
    screen.execute_instructions()

    print('# First question')
    print(f'Sum of signal strengths: {screen.sum}')
    
    print('# Second question')
    print('Screen output:')
    for row, line in enumerate(screen.output):
        print(f'({row}, {len(line)}) \'{line}\'')
   

if __name__ == '__main__':
    main()