""" Advent of Code 2022, Day 9, Part 2
    Author: Chi-Kit Pao
"""

import os

class Rope:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class RopeChain:
    def __init__(self, input_file_name: str):
        self.lines = []
        self.ropes = []
        self.rope_count = 10
        for i in range(0, self.rope_count):
            self.ropes.append(Rope(0, 0))
        self.tail_positions = set()
        self.add_tail_position()

        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            self.lines = list(map(lambda s: s.replace('\n', ''), f.readlines()))

    def add_tail_position(self):
        x = self.ropes[self.rope_count - 1].x
        y = self.ropes[self.rope_count - 1].y
        self.tail_positions.add(tuple([x, y]))

    def follow(self, rope_index):
        dx = self.ropes[rope_index - 1].x - self.ropes[rope_index].x
        dy = self.ropes[rope_index - 1].y - self.ropes[rope_index].y
        
        sign = lambda x: 1 if x > 0 else -1
        if abs(dx) == 2:
            if abs(dy) == 0:
                self.ropes[rope_index].x += sign(dx)
            elif abs(dy) == 1 or abs(dy) == 2:
                self.ropes[rope_index].x += sign(dx)
                self.ropes[rope_index].y += sign(dy)
            else:
                return
        elif abs(dy) == 2:
            if abs(dx) == 0:
                self.ropes[rope_index].y += sign(dy)
            elif abs(dx) == 1 or abs(dx) == 2:
                self.ropes[rope_index].y += sign(dy)
                self.ropes[rope_index].x += sign(dx)
            else:
                return
        else:
            return

        # Performed movement
        assert (abs(self.ropes[rope_index - 1].x - self.ropes[rope_index].x)<2 and abs(self.ropes[rope_index - 1].y - self.ropes[rope_index].y)<2)
        if rope_index == self.rope_count - 1:
            self.add_tail_position()
        else:
            self.follow(rope_index + 1)
    
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
        self.ropes[0].x += movement[0]
        self.ropes[0].y += movement[1]
        self.follow(1)

def main():
    print('# Second question')
    rope_chain = RopeChain('input1.txt')
    rope_chain.perform_movements()
    print(f'Number of tail positions: {len(rope_chain.tail_positions)}')
   

if __name__ == '__main__':
    main()
