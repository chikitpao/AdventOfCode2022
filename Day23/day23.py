""" Advent of Code 2022, Day 23
    Author: Chi-Kit Pao
"""


import os
import time
import typing as ty


def debug_output(message):
    # print(message)
    pass


class Elf:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.proposal_index_start = 0
        self.proposals = [self.try_north, self.try_south, self.try_west, \
            self.try_east]
        self.proposed_x = None
        self.proposed_y = None

    def move(self, quiz: "Quiz"):
        assert self.proposed_x is not None
        assert self.proposed_y is not None
        assert (self.x, self.y) in quiz.elf_pos, str(quiz.elf_pos) + ' ' + str(self.x) + ' ' + str(self.y)
        quiz.elf_pos.remove((self.x, self.y))
        self.x = self.proposed_x
        self.y = self.proposed_y
        quiz.elf_pos.add((self.x, self.y))

    def propose_step(self, quiz: "Quiz") -> ty.Tuple[int, int]:
        pos: ty.Tuple[int, int] = None
        self.proposed_x = None
        self.proposed_y = None

        is_alone = True
        for offset in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]:
            if quiz.is_occupied((self.x + offset[0], self.y + offset[1])):
                is_alone = False
                break

        if not is_alone:
            for i in range(self.proposal_index_start, self.proposal_index_start + 4):
                pos = self.proposals[(i % 4)](quiz)
                if pos is not None:
                    self.proposed_x, self.proposed_y = pos
                    break
        self.proposal_index_start = (self.proposal_index_start + 1 % 4)
        return self.proposed_step()

    def proposed_step(self) -> ty.Tuple[int, int]:
        if self.proposed_x is not None and self.proposed_y is not None:
            return self.proposed_x, self.proposed_y
        else:
            return None

    def try_east(self, quiz: "Quiz") -> ty.Tuple[int, int]:
        # 3 fields vacant in the east
        if quiz.is_occupied((self.x + 1,  self.y - 1)) or quiz.is_occupied((self.x + 1,  self.y)) \
            or quiz.is_occupied((self.x + 1,  self.y + 1)):
            return None
        return self.x + 1,  self.y

    def try_north(self, quiz: "Quiz") -> ty.Tuple[int, int]:
        # 3 fields vacant in the north
        if quiz.is_occupied((self.x - 1, self.y - 1)) or quiz.is_occupied((self.x, self.y - 1)) \
            or quiz.is_occupied((self.x + 1, self.y - 1)):
            return None
        return self.x, self.y - 1

    def try_south(self, quiz: "Quiz") -> ty.Tuple[int, int]:
        # 3 fields vacant in the south
        if quiz.is_occupied((self.x - 1, self.y + 1)) or quiz.is_occupied((self.x, self.y + 1)) \
            or quiz.is_occupied((self.x + 1, self.y + 1)):
            return None
        return self.x, self.y + 1

    def try_west(self, quiz: "Quiz") -> ty.Tuple[int, int]:
        # 3 fields vacant in the west
        if quiz.is_occupied((self.x - 1, self.y - 1)) or quiz.is_occupied((self.x - 1, self.y)) \
            or quiz.is_occupied((self.x - 1, self.y + 1)):
            return None
        return self.x - 1, self.y


class Quiz:
    def __init__(self, input_file_name: str):
        self.elves = []
        self.proposed_steps = {}  # pos -> count
        self.elf_pos = set()  # Positions of all elves
        self.__read_data(input_file_name)

    def add_proposed_step(self, pos: ty.Tuple[int, int]):
        if pos is None:
            return
        try:
            count = self.proposed_steps[pos]
            self.proposed_steps[pos] = count + 1
        except KeyError:
            self.proposed_steps[pos] = 1

    def is_blocked(self, pos: ty.Tuple[int, int]) -> bool:
        try:
            count = self.proposed_steps[pos]
            return count != 1
        except KeyError:
            assert False, 'Proposed step not found as such.'
            return False

    def is_occupied(self, pos: ty.Tuple[int, int]) -> bool:
        if pos in self.elf_pos:
            return True
        return False

    def run1(self) -> int:
        round = 1
        debug_output(f'start {self.elf_pos}')
        while True:
            movement_detected = False
            assert len(self.elves) == len(self.elf_pos)
            debug_output(f'round: {round}')
            self.proposed_steps.clear()
            # 1. Elves propose their step
            for elf in self.elves:
                self.add_proposed_step(elf.propose_step(self))
            # 2. Elves try to move
            for elf in self.elves:
                pos = elf.proposed_step()
                if pos is not None and not self.is_blocked(elf.proposed_step()):
                    elf.move(self)
                    movement_detected = True
            if not movement_detected:
                break
            elif round == 10:
                debug_output(f'{round} {self.elf_pos}')
                break
            debug_output(f'{round} {self.elf_pos}')
            round += 1

        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for elf in self.elves:
            min_x = elf.x if min_x is None else min(min_x, elf.x)
            max_x = elf.x if max_x is None else max(max_x, elf.x)
            min_y = elf.y if min_y is None else min(min_y, elf.y)
            max_y = elf.y if max_y is None else max(max_y, elf.y)
        return (max_x - min_x + 1) * (max_y - min_y + 1) - len(self.elves)

    def run2(self) -> int:
        round = 1
        debug_output(f'start {self.elf_pos}')
        while True:
            movement_detected = False
            assert len(self.elves) == len(self.elf_pos)
            debug_output(f'round: {round}')
            self.proposed_steps.clear()
            # 1. Elves propose their step
            for elf in self.elves:
                self.add_proposed_step(elf.propose_step(self))
            # 2. Elves try to move
            for elf in self.elves:
                pos = elf.proposed_step()
                if pos is not None and not self.is_blocked(elf.proposed_step()):
                    elf.move(self)
                    movement_detected = True
            if not movement_detected:
                return round
            debug_output(f'{round} {self.elf_pos}')
            round += 1 

    def __read_data(self, input_file_name: str):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', ''), f.readlines()))
            for row, line in enumerate(lines):
                for col, ch in enumerate(line):
                    if ch == '#':
                        self.elves.append(Elf(col, row))
                        self.elf_pos.add((col, row))


def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1
    quiz = Quiz(file_names[file_names_index])
    
    print('# First question')
    print(f'Empty ground tiles: {quiz.run1()}')

    start_time = time.time()
    print('# Second question')
    quiz = Quiz(file_names[file_names_index])
    print(f'Number of the first round where no Elf moves: {quiz.run2()}')
    print(f'Time elapsed: {time.time() - start_time} s')
    

if __name__ == '__main__':
    main()