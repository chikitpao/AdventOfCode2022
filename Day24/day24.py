""" Advent of Code 2022, Day 24
    Author: Chi-Kit Pao
    REMARK: Requires Python 3.9 or later due to usage of math.lcm()
"""

import math
import os
import time
import typing as ty


def debug_output(message):
    # print(message)
    pass


class Quiz:
    def __init__(self, input_file_name: str):
        self.maps = [] # time, row, column
        self.rows = 0
        self.columns = 0
        self.__read_data(input_file_name)
        self.upper_pos = (0, self.maps[0][0].index('.'))
        self.lower_pos = (self.rows - 1, self.maps[0][self.rows - 1].index('.'))
        self.__generate_map_sequence()

    def run(self, forward: bool, start_time):
        minute = start_time
        start_pos = self.upper_pos if forward else self.lower_pos
        end_pos = self.lower_pos if forward else self.upper_pos
        visited_old = {(0,  start_pos[0], start_pos[1])}
        while True:
            minute += 1
            visited = set()
            maps_length = len(self.maps)
            for node in visited_old:
                # visit right, down, left, up
                test_positions = [(node[1], node[2] + 1), (node[1] + 1, node[2]), \
                    (node[1], node[2] - 1), (node[1] - 1, node[2]), (node[1], node[2])]
                for test_pos in test_positions:
                    if test_pos[0] < 0 or test_pos[0] >= self.rows:
                        continue
                    if test_pos[1] <= 0 or test_pos[1] >= self.columns - 1:
                        continue
                    if self.maps[minute % maps_length][test_pos[0]][test_pos[1]] == '.':
                        if test_pos == end_pos:
                            return minute
                        visited.add((minute, test_pos[0], test_pos[1]))
            visited_old = visited

    def __generate_map_sequence(self):
        blizzard_rows = self.rows - 2
        blizzard_columns = self.columns - 2
        
        # time [0 to columns - 2], direction [LEFT, RIGHT], row, column
        horizontal_maps = [[[], []]]
        horizontal_maps[0][0].append(self.maps[0][0])
        horizontal_maps[0][1].append(self.maps[0][0])
        for row in range(1, self.rows - 1):
            horizontal_maps[0][0].append(self.maps[0][row].replace('>', '.').replace('^', '.').replace('v', '.'))
            horizontal_maps[0][1].append(self.maps[0][row].replace('<', '.').replace('^', '.').replace('v', '.'))
        horizontal_maps[0][0].append(self.maps[0][self.rows - 1])
        horizontal_maps[0][1].append(self.maps[0][self.rows - 1])
        for i in range(1, blizzard_columns + 1):
            horizontal_maps.append([[], []])
            horizontal_maps[i][0].append(self.maps[0][0])
            horizontal_maps[i][1].append(self.maps[0][0])
            for row in range(1, self.rows - 1):
                horizontal_maps[i][0].append(''.join([horizontal_maps[i - 1][0][row][0], \
                    horizontal_maps[i - 1][0][row][2: self.columns - 1], \
                    horizontal_maps[i - 1][0][row][1], \
                    horizontal_maps[i - 1][0][row][self.columns - 1]]))
                horizontal_maps[i][1].append(''.join([horizontal_maps[i - 1][1][row][0], \
                    horizontal_maps[i - 1][1][row][self.columns - 2], \
                    horizontal_maps[i - 1][1][row][1:(self.columns - 2)], \
                    horizontal_maps[i - 1][1][row][self.columns - 1]]))
            horizontal_maps[i][0].append(self.maps[0][self.rows - 1])
            horizontal_maps[i][1].append(self.maps[0][self.rows - 1])

        # time [0 to rows - 2], direction [UP, DOWN], row, column
        vertical_maps = [[[], []]]
        vertical_maps[0][0].append(self.maps[0][0])
        vertical_maps[0][1].append(self.maps[0][0])
        for row in range(1, self.rows - 1):
             vertical_maps[0][0].append(self.maps[0][row].replace('v', '.').replace('<', '.').replace('>', '.'))
             vertical_maps[0][1].append(self.maps[0][row].replace('^', '.').replace('<', '.').replace('>', '.'))
        vertical_maps[0][0].append(self.maps[0][self.rows - 1])
        vertical_maps[0][1].append(self.maps[0][self.rows - 1])
        for i in range(1, blizzard_rows + 1):
            vertical_maps.append([[], []])
            vertical_maps[i][0].append(self.maps[0][0])
            vertical_maps[i][1].append(self.maps[0][0])
            vertical_maps[i][0].append(vertical_maps[i - 1][0][2])
            vertical_maps[i][1].append(vertical_maps[i - 1][1][self.rows - 2])
            for row in range(2, self.rows - 2):
                vertical_maps[i][0].append(vertical_maps[i - 1][0][row + 1])
                vertical_maps[i][1].append(vertical_maps[i - 1][1][row - 1])
            vertical_maps[i][0].append(vertical_maps[i - 1][0][1])
            vertical_maps[i][1].append(vertical_maps[i - 1][1][self.rows - 3])
            vertical_maps[i][0].append(self.maps[0][self.rows - 1])
            vertical_maps[i][1].append(self.maps[0][self.rows - 1])
       
        lcm = math.lcm(blizzard_rows, blizzard_columns)
        for minute in range(1, lcm):
            self.maps.append([])
            self.maps[-1].append(self.maps[0][0])
            for row in range(1, self.rows - 1):
                char_list = [None] * self.columns
                char_list[0] = '#'
                char_list[self.columns - 1] = '#'
                for i in range(1, blizzard_columns + 1):
                    temp_list = []
                    if horizontal_maps[minute % blizzard_columns][0][row][i] != '.':
                        temp_list.append(horizontal_maps[minute % blizzard_columns][0][row][i])
                    if horizontal_maps[minute % blizzard_columns][1][row][i] != '.':
                        temp_list.append(horizontal_maps[minute % blizzard_columns][1][row][i])
                    if vertical_maps[minute % blizzard_rows][0][row][i] != '.':
                        temp_list.append(vertical_maps[minute % blizzard_rows][0][row][i])
                    if vertical_maps[minute % blizzard_rows][1][row][i] != '.':
                        temp_list.append(vertical_maps[minute % blizzard_rows][1][row][i])
                    if len(temp_list) == 0:
                        char_list[i] = '.'
                    elif len(temp_list) == 1:
                        char_list[i] = temp_list[0]
                    else:
                        char_list[i] = chr(ord('0') + len(temp_list))
                self.maps[-1].append(''.join(char_list))
            self.maps[-1].append(self.maps[0][self.rows - 1])

    def __read_data(self, input_file_name: str):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', ''), f.readlines()))
            self.maps.append(lines)
            self.rows = len(lines)
            self.columns = len(lines[0])

    def __print_map(self, title: str, map):
        print(title)
        for row in map:
            print(row)


def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1
    # test: 6 rows x 8 columns
    # input1: 27 rows x 122 columns

    start_time = time.time()
    quiz = Quiz(file_names[file_names_index])
    print('# First question')
    time1 = quiz.run(True, 0)
    print(f'Minutes required to reach the goal: {time1}')
    print(f'Time elapsed: {time.time() - start_time} s')
    
    start_time = time.time()
    print('# Second question')
    time2 = quiz.run(False, time1)
    time3 = quiz.run(True, time2)
    print(f'Minutes required to go foward, backward, and forward: {time3}')
    print(f'Time elapsed: {time.time() - start_time} s')

if __name__ == '__main__':
    main()