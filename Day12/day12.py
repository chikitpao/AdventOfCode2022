""" Advent of Code 2022, Day 12
    Author: Chi-Kit Pao
"""

import os

def debug_output(message):
    #print(message)
    pass

class Cell:
    UNVISITED = 0
    VISITING = 1
    VISITED = 2

    N = 0
    E = 1
    S = 2
    W = 3
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.state = Cell.UNVISITED
        self.distance = float('inf')
        self.pred = None
        self.neighbors = []
        for _ in range(4):
            self.neighbors.append(None)

    def add_neighbors(self, north, west):
        if north is not None:
            self.neighbors[Cell.N] = north
            north.neighbors[Cell.S] = self
        if west is not None:
            self.neighbors[Cell.W]  = west
            west.neighbors[Cell.E]  = self


class ElevationMap:
    def __init__(self, input_file_name: str):
        self.width = 0
        self.height = 0
        self.cells = []
        self.start_cell = None
        self.end_cell = None
        self.candidates = []
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            self.width = len(lines[0])
            self.height = len(lines) if len(lines[-1]) > 0 else len(lines) - 1
            for i in range(self.height):
                current_row = []
                self.cells.append(current_row)
                for j in range(self.width):
                    value = lines[i][j]
                    cell = Cell(i, j, value)
                    current_row.append(cell)

                    north = None if i == 0 else self.cells[i-1][j]
                    west = None if j == 0 else self.cells[i][j-1]
                    cell.add_neighbors(north, west)

                    if value == 'S':
                        cell.height = ord('a')
                        self.start_cell = cell
                    elif value == 'E':
                        self.end_cell = cell
                        cell.height = ord('z')
                    else:
                        cell.height = ord(cell.value)

    def find_route(self):
        self.start_cell.state = Cell.VISITING
        self.start_cell.distance = 0.0
        self.candidates.append(self.start_cell)

        while len(self.candidates) > 0:
            # process best candidate
            best_candidate = None
            for c in self.candidates:
                if best_candidate is None:
                    best_candidate = c
                else:
                    if c.distance < best_candidate.distance:
                        best_candidate = c

            if best_candidate == self.end_cell:
                debug_output(f'self.end_cell {self.end_cell.row} {self.end_cell.col} pred {self.end_cell.pred.row} {self.end_cell.pred.col}')
                print(f'Found route! Distance: {best_candidate.distance}')
                return
            
            processed = self.process(best_candidate, True)
            debug_output(f'({best_candidate.row},{best_candidate.col}) processed {processed} cells.')
            self.candidates.remove(best_candidate)

    def find_route_backward(self):
        self.end_cell.state = Cell.VISITING
        self.end_cell.distance = 0.0
        self.candidates.append(self.end_cell)

        while len(self.candidates) > 0:
            # process best candidate
            best_candidate = None
            for c in self.candidates:
                if best_candidate is None:
                    best_candidate = c
                else:
                    if c.distance < best_candidate.distance:
                        best_candidate = c
                    elif c.distance == best_candidate.distance and c.height < best_candidate.height:
                        best_candidate = c

            if best_candidate.height == ord('a'):
                debug_output(f'start cell {best_candidate.row} {best_candidate.col} pred {best_candidate.pred.row} {best_candidate.pred.col}')
                print(f'Found route! Distance: {best_candidate.distance}. Start cell ({best_candidate.row},{best_candidate.col})')
                return
            
            processed = self.process(best_candidate, False)
            debug_output(f'({best_candidate.row},{best_candidate.col}) processed {processed} cells.')
            self.candidates.remove(best_candidate)

    def process(self, cell, forward):
        debug_output(f'Processing ({cell.row},{cell.col}). State {cell.state}.')
        assert (cell.state == Cell.VISITING)

        processed = 0
        for i in range(4):
            if self.visit(cell, cell.neighbors[i], forward):
                processed += 1

        cell.state = Cell.VISITED
        return processed

    def visit(self, cell, other, forward):
        if other is None or other.state == Cell.VISITED:
            return False

        if forward:
            if cell.height + 1 < other.height:
                return False
        else:
            if cell.height - 1 > other.height:
                return False

        debug_output(f'Visiting ({other.row},{other.col}). State {other.state}.')

        if other.state == Cell.UNVISITED:
            other.pred = cell
            other.distance = cell.distance + 1.0
            other.state = Cell.VISITING
            self.candidates.append(other)
        else:
            assert other.state == Cell.VISITING and other.pred is not None
            temp_distance = cell.distance + 1.0
            if temp_distance < other.distance:
                other.pred = cell
                other.distance = temp_distance
        return True

def main():
    
    print('# First question')
    elevationMap = ElevationMap('input1.txt')
    elevationMap.find_route()
    
    print('# Second question')
    elevationMap = ElevationMap('input1.txt')
    elevationMap.find_route_backward()
   

if __name__ == '__main__':
    main()