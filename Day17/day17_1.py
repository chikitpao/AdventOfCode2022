""" Advent of Code 2022, Day 17, Part 1
    Author: Chi-Kit Pao
"""


import os


def debug_output(message):
    # print(message)
    pass


class RockTemplate:
    def __init__(self, width, height, shape):
        self.width = width
        self.height = height
        self.shape = shape


class Rock:
    def __init__(self, puzzle, template_index, x, y):
        # x, y are bottom left coordinates
        self.puzzle = puzzle
        self.template_index = template_index
        self.left = x
        self.bottom = y
        self.width = puzzle.rock_templates[self.template_index].width
        self.height = puzzle.rock_templates[self.template_index].height

    def check_stopped(self):
        # Check movement possible with situation in map
        if self.puzzle.check_row_occupied(self.bottom - 1, self.left, self.puzzle.rock_templates[self.template_index]):
            self.puzzle.highest_obstacle_row = max(self.bottom + self.height - 1, self.puzzle.highest_obstacle_row)
            # Put rock into map
            self.puzzle.put_rock_into_map(self)
            # Update puzzle.map_last_line_y if necessary
            self.puzzle.update_map_last_line()
            self.puzzle = None
            return True
        return False

    def fall(self):
        self.bottom -= 1
        self.move_x(self.puzzle.jet_stream_line[self.puzzle.current_jet_pattern_index])
        self.puzzle.current_jet_pattern_index = (self.puzzle.current_jet_pattern_index + 1) % self.puzzle.jet_stream_line_length                

    def get_coordinates_string(self):
        return f'({self.left}, {self.bottom + self.height - 1}) ({self.left + self.width - 1}, {self.bottom})'

    def move_x(self, jet_stream):
        if(jet_stream == '<'):
            if not self.puzzle.check_column_occupied(self.bottom, self.left, self.puzzle.rock_templates[self.template_index], True):
                self.left -= 1
        elif (jet_stream == '>'):
            if not self.puzzle.check_column_occupied(self.bottom, self.left, self.puzzle.rock_templates[self.template_index], False):
                self.left += 1
        else:
            raise ValueError(f'Unknown jet stream {jet_stream}')


class Puzzle:
    TUNNEL_WIDTH = 7
    MAP_WIDTH = TUNNEL_WIDTH + 2
    MAP_HEIGHT = 1000

    SPACE = '.'
    BOUNDARY = '+'
    ROCK_1 = '1'
    ROCK_2 = '2'
    ROCK_3 = '3'
    ROCK_4 = '4'
    ROCK_5 = '5'

    def __init__(self, input_file_name: str):
        # Possible x values [0, 6]
        # Possible y values [1, oo)

        self.rock_templates = []
        # REMARK: Reordered rocks to first rock will have index 1
        self.rock_templates.append(RockTemplate(2, 2, '5555'))
        self.rock_templates.append(RockTemplate(4, 1, '1111'))
        self.rock_templates.append(RockTemplate(3, 3, '.2.222.2.'))
        self.rock_templates.append(RockTemplate(3, 3, '..3..3333'))
        self.rock_templates.append(RockTemplate(1, 4, '4444'))
        self.current_rock_index = 0
        self.map = []
        self.map_last_line_y = 0  # y coordinate of self.map[Puzzle.MAP_HEIGHT - 1]
        self.highest_obstacle_row = 0  # initially the ground, then the top row of the highest rock

        self.__create_map()
        self.__read_jet_pattern(input_file_name)  # length 40, 10091
        self.current_jet_pattern_index = 0

    def check_column_occupied(self, row, column, rock_template, isLeft):
        map_y = self.__global_y_to_map_y(row)
        x_offset = -1 if isLeft else 1
        for i in range(rock_template.height):
            for j in range(rock_template.width):
                char = rock_template.shape[i * rock_template.width + j]
                if char == Puzzle.SPACE:
                    continue
                if self.map[map_y - rock_template.height + 1 + i][column + j + x_offset] != Puzzle.SPACE:
                    return True
        return False

    def check_row_occupied(self, rock_next_y, column, rock_template):
        map_y = self.__global_y_to_map_y(rock_next_y)
        for i in range(rock_template.height):
            for j in range(rock_template.width):
                char = rock_template.shape[i * rock_template.width + j]
                if char == Puzzle.SPACE:
                    continue
                if self.map[map_y - rock_template.height + 1 + i][column + j] != Puzzle.SPACE:
                    return True
        return False

    def drop_rock(self):
        self.current_rock_index += 1
        rock = Rock(self, self.current_rock_index % len(self.rock_templates), 1 + 2, self.highest_obstacle_row + 4)
        rock.move_x(self.jet_stream_line[self.current_jet_pattern_index])
        self.current_jet_pattern_index = (self.current_jet_pattern_index + 1) % self.jet_stream_line_length
        return rock

    def print_map(self, start_y, end_y, global_y = False):
        if global_y:
            map_start_y =  self.__global_y_to_map_y(end_y) + 1
            map_end_y =  self.__global_y_to_map_y(start_y) + 1
            for i in range(map_start_y, map_end_y):
                if i == Puzzle.MAP_HEIGHT - 1:
                     print(self.map[i], self.map_last_line_y)
                     break
                elif i == map_start_y:
                    print(self.map[i], end_y - 1)
                elif i + 1 == map_end_y:
                    print(self.map[i], start_y)
                else:
                    print(self.map[i])
        else:
            for i in range(start_y, end_y):
                if i == Puzzle.MAP_HEIGHT - 1:
                    print(self.map[i], Puzzle.MAP_HEIGHT - 1)
                    break
                elif i == start_y or i + 1 == end_y:
                    print(self.map[i], i)
                else:
                    print(self.map[i])

    def put_rock_into_map(self, rock):
        map_start_y = self.__global_y_to_map_y(rock.bottom + rock.height - 1)
        rock_template = self.rock_templates[rock.template_index]
        for i in range(rock.height):
            map_y = map_start_y + i
            for j in range(rock.width):
                map_x = rock.left + j
                char = rock_template.shape[i * rock.width + j]
                if  char != Puzzle.SPACE:
                    assert (self.map[map_y][map_x] == Puzzle.SPACE), f'{map_y} {map_x} {self.map[map_y][map_x]}'
                    self.map[map_y][map_x] = char
                    debug_output(f'({map_y}, {map_x}) -> {char}')

    def run(self, end):
        while self.current_rock_index < end:
            rock = self.drop_rock()
            while not rock.check_stopped():
                rock.fall()
            debug_output(f'rock {self.current_rock_index}:  {rock.get_coordinates_string()}')
     
    def update_map_last_line(self):
        map_y = self.__global_y_to_map_y(self.highest_obstacle_row)
        if map_y < 10:
            half_height = Puzzle.MAP_HEIGHT // 2
            del self.map[half_height:]
            for _ in range(half_height):
                row = [Puzzle.SPACE] * Puzzle.MAP_WIDTH
                row[0] = Puzzle.BOUNDARY
                row[Puzzle.MAP_WIDTH - 1] = Puzzle.BOUNDARY
                self.map.insert(0, row)
            self.map_last_line_y += half_height

    def __create_map(self):
        for _ in range(Puzzle.MAP_HEIGHT - 1):
            row = [Puzzle.SPACE] * Puzzle.MAP_WIDTH
            row[0] = Puzzle.BOUNDARY
            row[Puzzle.MAP_WIDTH - 1] = Puzzle.BOUNDARY
            self.map.append(row)
        row = [Puzzle.BOUNDARY] * Puzzle.MAP_WIDTH
        self.map.append(row)

    def __read_jet_pattern(self, input_file_name):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            self.jet_stream_line = f.readline().replace('\n', '')
            self.jet_stream_line_length = len(self.jet_stream_line)
            print('jet_stream_line_length', self.jet_stream_line_length)

    def __global_y_to_map_y(self, global_y):
        return Puzzle.MAP_HEIGHT - 1 - (global_y - self.map_last_line_y)

def main():
    puzzle = Puzzle('input1.txt')

    print('# First question')
    puzzle.run(2022)
    puzzle.print_map(puzzle.highest_obstacle_row - 10, puzzle.highest_obstacle_row + 1, global_y = True)


if __name__ == '__main__':
    main()