""" Advent of Code 2022, Day 9, Part 1
    Author: Chi-Kit Pao
"""

import os


class Rope:
    def __init__(self, input_file_name: str):
        self.lines = []
        self.head = [0, 0]
        self.tail = [0, 0]
        self.tail_positions = set()
        self.tail_positions.add(tuple(self.tail))

        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            self.lines = list(map(lambda s: s.replace('\n', ''), f.readlines()))
    
    def perform_movements(self):
        movements = {'L': [-1, 0], 'R': [1, 0], 
                    'U': [0, 1], 'D': [0, -1]}
        for line in self.lines:
            instruction = line.split()
            if len(instruction) != 2:
                continue
            steps = int(instruction[1])
            for i in range(0, steps):
                self.move(movements[instruction[0]])
    
    def move(self, movement):
        # Rules:
        # 1. Move head and place tail behind head (opposite to movement) if
        #    tail is behind head (left behind, behind, or right behind).
        # 2. Otherwise only move head
        if movement[0] != 0:  # horizontal movement
            if self.tail[0] == self.head[0] - movement[0]:
                self.head[0] += movement[0]
                self.tail[0] = self.head[0] - movement[0]
                self.tail[1] = self.head[1]
                self.tail_positions.add(tuple(self.tail))
            else:
                self.head[0] += movement[0]
        elif movement[1] != 0:  # vertical movement
            if self.tail[1] == self.head[1] - movement[1]:
                self.head[1] += movement[1]
                self.tail[1] = self.head[1] - movement[1]
                self.tail[0] = self.head[0]
                self.tail_positions.add(tuple(self.tail))
            else:
                self.head[1] += movement[1]


def main():
    print('# First question')
    rope = Rope('input1.txt')
    rope.perform_movements()
    print(f'Number of tail positions: {len(rope.tail_positions)}')
   

if __name__ == '__main__':
    main()