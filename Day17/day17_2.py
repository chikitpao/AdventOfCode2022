""" Advent of Code 2022, Day 17, Part 2
    Author: Chi-Kit Pao
"""


import os
import signal

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
        #if self.puzzle.current_rock_index % 5 == 1:
        #    debug_output(f'fall: selfpuzzle..current_rock_index {self.puzzle.current_rock_index} ' + \
        #     f'self.puzzle.current_jet_pattern_index {self.puzzle.current_jet_pattern_index} {self.puzzle.current_jet_pattern_index % self.puzzle.jet_stream_line_length}')
        self.bottom -= 1
        self.move_x(self.puzzle.jet_stream_line[self.puzzle.current_jet_pattern_index % self.puzzle.jet_stream_line_length])
        self.puzzle.current_jet_pattern_index = self.puzzle.current_jet_pattern_index + 1             

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
        self.state_hash = {}  # state hash -> list of tuples (next_rock_index, current_jet_pattern_index, highest_obstacle_row)
        self.__rows_to_check = 1  # number of rows to be checked for cyclic pattern, set by method run
        self.found_cyclic_pattern = False
        self.__end = 0  # set by method run

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
        assert self.current_rock_index <= self.__end
        if self.current_rock_index == self.__end:
            debug_output(f'last rock, index {self.current_rock_index % 5}')
        rock = Rock(self, self.current_rock_index % len(self.rock_templates), 1 + 2, self.highest_obstacle_row + 4)
        rock.move_x(self.jet_stream_line[self.current_jet_pattern_index % self.jet_stream_line_length])
        self.current_jet_pattern_index = self.current_jet_pattern_index + 1
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
                    # debug_output(f'({map_y}, {map_x}) -> {char}')

    def run(self, end, rows_to_check):
        print(f'Puzzle.run with end = {end}')
        self.__end = end
        self.__rows_to_check = rows_to_check
        while self.current_rock_index < self.__end:
            if not self.found_cyclic_pattern:
                state = self.__handle_cyclic_state()
                if self.current_rock_index == self.__end:
                    break;
            rock = self.drop_rock()
            while not rock.check_stopped():
                rock.fall()
            # debug_output(f'rock {self.current_rock_index}: {rock.get_coordinates_string()}')
     
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

    def __calculate_map_state_hash(self):
        state_hash = 0
        map_y = self.__global_y_to_map_y(self.highest_obstacle_row)
        current_factor = 1        
        for row in range(map_y, map_y + self.__rows_to_check):
            if row >= Puzzle.MAP_HEIGHT:
                break
            for j in range(1, 8):
                if self.map[row][j] == Puzzle.SPACE:
                    pass
                elif self.map[row][j] == Puzzle.BOUNDARY:
                    pass
                else:
                    digit = ord(self.map[row][j]) - ord('1') + 1
                    assert digit >= 1 and digit <= 5
                    state_hash += digit * current_factor
                current_factor *= 10
        return state_hash

    def __create_map(self):
        for _ in range(Puzzle.MAP_HEIGHT - 1):
            row = [Puzzle.SPACE] * Puzzle.MAP_WIDTH
            row[0] = Puzzle.BOUNDARY
            row[Puzzle.MAP_WIDTH - 1] = Puzzle.BOUNDARY
            self.map.append(row)
        row = [Puzzle.BOUNDARY] * Puzzle.MAP_WIDTH
        self.map.append(row)

    def __get_row_data_from_hash(self, state_hash):
        temp_state_hash = state_hash
        divisor = 10**7
        while temp_state_hash > 0:
            remainder = temp_state_hash % divisor
            temp_state_hash = temp_state_hash // divisor
            row_data = ['+']
            for i in range(7):
                remainder_remainder = remainder % 10
                if remainder_remainder == 0:
                    row_data.append('.')
                else:
                    row_data.append(chr(ord('1') + remainder_remainder - 1))
                remainder = remainder // 10
            row_data.append('+')
            yield row_data


    def __handle_cyclic_state(self):
        if self.current_rock_index == 0:
            return None
        next_rock_index = self.current_rock_index + 1
        state_hash = self.__calculate_map_state_hash()
        try:
            hashed_states = self.state_hash[state_hash]
            for item in hashed_states:
                previous_next_rock_index = item[0]
                previous_jet_pattern_index = item[1]
                previous_highest_obstacle_row = item[2]
                next_rock_index_difference = next_rock_index - previous_next_rock_index
                jet_pattern_index_difference = self.current_jet_pattern_index - previous_jet_pattern_index
                if next_rock_index_difference % 5 == 0 and jet_pattern_index_difference % self.jet_stream_line_length == 0:
                    # Found cyclic pattern
                    print(f'Found cycle (rows to check = {self.__rows_to_check}):')
                    print(f'next rock index {next_rock_index}, {previous_next_rock_index}, difference {next_rock_index_difference}')
                    print(f'jet pattern index {self.current_jet_pattern_index}, {previous_jet_pattern_index}, difference {jet_pattern_index_difference}')
                    highest_obstacle_row_difference =  self.highest_obstacle_row - previous_highest_obstacle_row
                    print(f'highest obstacle row {self.highest_obstacle_row}, {previous_highest_obstacle_row}, difference {highest_obstacle_row_difference}')
                    print('# Map when cycle was detected:')
                    self.print_map(self.highest_obstacle_row - self.__rows_to_check + 1, self.highest_obstacle_row + 1, global_y = True)        
                    self.found_cyclic_pattern = True

                    # Calculate remaining state after evaluating applying cyclic patterns
                    remaining_cycles = (self.__end - self.current_rock_index) // next_rock_index_difference
                    r = (self.current_rock_index) % next_rock_index_difference
                    debug_output(f'remaining_cycles {remaining_cycles}')
                    debug_output(f'remainder {r} last rock {(next_rock_index + r - 1) % 5}')
                    new_current_rock_index = self.current_rock_index + remaining_cycles * next_rock_index_difference
                    new_jet_pattern_index = self.current_jet_pattern_index + remaining_cycles * jet_pattern_index_difference
                    new_highest_obstacle_row = self.highest_obstacle_row + remaining_cycles * highest_obstacle_row_difference
                    # # Recreate map with pattern found
                    # self.map = []
                    # self.highest_obstacle_row = 0
                    # self.map_last_line_y = 0
                    # self.__create_map()
                    # Finish new map
                    # gen = self.__get_row_data_from_hash(state_hash)
                    # for i, row_data in enumerate(gen):
                    #     self.map[Puzzle.MAP_HEIGHT - self.__rows_to_check - 1 + i] = row_data
                    #     print(i, row_data)
                    # Update rock index & jet pattern index & heightes_obstacle_row
                    self.current_rock_index = new_current_rock_index
                    self.current_jet_pattern_index = new_jet_pattern_index
                    self.highest_obstacle_row = new_highest_obstacle_row
                    self.map_last_line_y += remaining_cycles * highest_obstacle_row_difference
                    print('# Map after cycle related modification:')
                    self.print_map(self.highest_obstacle_row - self.__rows_to_check + 1, self.highest_obstacle_row + 1, global_y = True)        

                    return item
            self.state_hash[state_hash].append((next_rock_index, self.current_jet_pattern_index, self.highest_obstacle_row))
            return None
        except KeyError:
            self.state_hash[state_hash] = []
            self.state_hash[state_hash].append((next_rock_index, self.current_jet_pattern_index, self.highest_obstacle_row))
            return None

    def __read_jet_pattern(self, input_file_name):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            self.jet_stream_line = f.readline().replace('\n', '')
            self.jet_stream_line_length = len(self.jet_stream_line)
            print('jet_stream_line_length', self.jet_stream_line_length)

    def __global_y_to_map_y(self, global_y):
        return Puzzle.MAP_HEIGHT - 1 - (global_y - self.map_last_line_y)


g_puzzle = None


def sigbreak_handler(signum, frame):
    global g_puzzle
    print(f'self.current_rock_index {g_puzzle.current_rock_index}, current_jet_pattern_index {g_puzzle.current_jet_pattern_index}')


def main():
    file_names = ['test.txt', 'input1.txt']
    rocks_count = [2022, 1_000_000_000_000]
    file_names_index = 1
    rocks_count_index = 1

    print('# Second question')
    puzzle = Puzzle(file_names[file_names_index]) 
    global g_puzzle
    g_puzzle = puzzle
    # SIGBREAK only works on Windows (Ctrl + Break). Not needed for correct implementation.
    signal.signal(signal.SIGBREAK, sigbreak_handler)
    rows_to_check = 20
    puzzle.run(rocks_count[rocks_count_index], rows_to_check)
    print('# Final map')
    puzzle.print_map(puzzle.highest_obstacle_row - rows_to_check + 1, puzzle.highest_obstacle_row + 1, global_y = True)


if __name__ == '__main__':
    main()