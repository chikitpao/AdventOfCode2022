""" Advent of Code 2022, Day 14, Part 1
    Author: Chi-Kit Pao
"""

import os


def debug_output(message):
    print(message)
    #pass


class Reservoir:
    AIR = 0
    ROCK = 1
    SOURCE = 2
    SAND = 3
    character = { AIR: '.', ROCK: '#', SOURCE: '+', SAND: 'o' }
    
    def __init__(self, input_file_name: str, width_factor):
        self.x_source = 500
        self.y_source = 0
        self.x_min = self.x_source 
        self.x_max = self.x_source 
        self.y_min = self.y_source
        self.y_max = self.y_source
        self.map = []
        self.sand_map = []
        self.sand_count = 0
        self.corner_coordinates = []
        self.width_factor = width_factor

        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            for line in lines:
                if len(line) > 0:
                    coordinates_strings = line.replace('-> ', '').split()
                    corner_coordinates_row = []
                    for s in coordinates_strings:
                        corner_coordinates_row.append(list(map(lambda s: int(s), s.split(','))))
                    for c in corner_coordinates_row:
                        x = c[0]
                        self.x_min = min(self.x_min, x)
                        self.x_max = max(self.x_max, x)
                        y = c[1]
                        self.y_min = min(self.y_min, y)
                        self.y_max = max(self.y_max, y)
                        self.corner_coordinates.append(corner_coordinates_row)
            self.y_max += 2
            self.x_min = min(self.x_min, self.x_source - self.y_max * self.width_factor) - 10
            self.x_max = max(self.x_max, self.x_source + self.y_max * self.width_factor) + 10
            print(f'x_min {self.x_min}, x_max: {self.x_max}')
            self.rel_x_source = self.x_source - self.x_min
            self.rel_y_source = self.y_source - self.y_min
            self.width = self.x_max - self.x_min + 1
            self.height = self.y_max + 1
            self.__create_map()      


    def print_map(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == Reservoir.AIR:
                    print(Reservoir.character[self.sand_map[i][j]], end='')
                else:
                    print(Reservoir.character[self.map[i][j]], end='')
            print('')
    
    def run(self):
        for _ in range(self.height):
            row = [Reservoir.AIR] * self.width
            self.sand_map.append(row)

        sand = [self.rel_y_source, self.rel_x_source]

        while sand[0] + 1 < self.height:  # self.height - 1 -> ground
            assert sand[0] + 1 < self.height
            
            # source is blocked
            if self.sand_map[sand[0]][sand[1]] == Reservoir.SAND:
                return True

            if self.map[sand[0] + 1][sand[1]] != Reservoir.ROCK and self.sand_map[sand[0] + 1][sand[1]] != Reservoir.SAND:
                sand[0] += 1
                continue
            
            if sand[1] - 1 < 0:
                raise ValueError()
            elif self.map[sand[0] + 1][sand[1] - 1] != Reservoir.ROCK and self.sand_map[sand[0] + 1][sand[1] - 1] != Reservoir.SAND:
                sand[0] += 1
                sand[1] -= 1
                continue

            if sand[1] + 1 >= self.width:
                raise ValueError()
            elif self.map[sand[0] + 1][sand[1] + 1] != Reservoir.ROCK and self.sand_map[sand[0] + 1][sand[1] + 1] != Reservoir.SAND:
                sand[0] += 1
                sand[1] += 1
                continue

            self.sand_map[sand[0]][sand[1]] = Reservoir.SAND
            self.sand_count += 1
            # new unit of sand
            sand = [self.rel_y_source, self.rel_x_source]

        # Actually unreachable
        return False
    
    def __add_rock(self, corner_coordinates_row, index):
        corner_coordinates1 = corner_coordinates_row[index]
        corner_coordinates2 = corner_coordinates_row[index + 1]
        if corner_coordinates1[0] == corner_coordinates2[0]:
            x = corner_coordinates1[0]
            rel_x = x - self.x_min
            step = 1 if corner_coordinates1[1] <= corner_coordinates2[1] else -1
            for rel_y in range(corner_coordinates1[1] - self.y_min, corner_coordinates2[1] - self.y_min + step, step):
                self.map[rel_y][rel_x] = Reservoir.ROCK  
        else:
            assert corner_coordinates1[1] == corner_coordinates2[1]
            y = corner_coordinates1[1]
            rel_y = y - self.y_min
            step = 1 if corner_coordinates1[0] <= corner_coordinates2[0] else -1
            for rel_x in range(corner_coordinates1[0] - self.x_min, corner_coordinates2[0] - self.x_min + step, step):
                self.map[rel_y][rel_x] = Reservoir.ROCK

    def __create_map(self):
        for _ in range(self.height):
            row = [Reservoir.AIR] * self.width
            self.map.append(row)
        self.map[self.rel_y_source][self.rel_x_source] = Reservoir.SOURCE
        for corner_coordinates_row in self.corner_coordinates:
            for i in range(len(corner_coordinates_row) - 1):
                self.__add_rock(corner_coordinates_row, i)

        for i in range(0, self.width):
            self.map[self.height - 1][i] = Reservoir.ROCK


def main():
    
    print('# Second question')
    width_factor = 1
    succeeded = False
    while not succeeded:
        try:
            reservoir = Reservoir('input1.txt', width_factor)
            if(reservoir.run()):
                succeeded = True
            reservoir.print_map()
            print(f'Units of sand: {reservoir.sand_count}')
        except ValueError:
            # REMARK: ValueError not raised at all. Got result with width_factor = 1.
            print(f'Failed with width factor {width_factor}!')
            width_factor += 1


if __name__ == '__main__':
    main()