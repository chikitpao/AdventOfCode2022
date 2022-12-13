""" Advent of Code 2022, Day 8
    Author: Chi-Kit Pao
"""

import os


class Woods:
    def __init__(self, input_file_name: str):
        file_path = os.path.dirname(__file__)
        self.rows = []
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            self.rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))
        
        self.row_count = len(self.rows)  # Somehow no empty line at the end
        self.col_count = len(self.rows[0])

    def count_visible_trees(self):
        count = 0
        for i in range(0, self.row_count):
            for j in range(0, self.col_count):
                if self.is_tree_visible(i, j):
                    count += 1
        return count

    def is_visible_from_left(self, row, col):
        own_height = int(self.rows[row][col])
        for j in range(0, col):
            if int(self.rows[row][j]) >= own_height:
                return False
        return True

    def is_visible_from_right(self, row, col):
        own_height = int(self.rows[row][col])
        for j in range(col + 1, self.col_count):
            if int(self.rows[row][j]) >= own_height:
                return False
        return True

    def is_visible_from_top(self, row, col):
        own_height = int(self.rows[row][col])
        for i in range(0, row):
            if int(self.rows[i][col]) >= own_height:
                return False
        return True

    def is_visible_from_bottom(self, row, col):
        own_height = int(self.rows[row][col])
        for i in range(row + 1, self.row_count):
            if int(self.rows[i][col]) >= own_height:
                return False
        return True

    def is_tree_visible(self, row, col):
        assert ((row >= 0) and (row < self.row_count) and (col >= 0) and (col < self.col_count))

        if row == 0 or (row + 1) == self.row_count:
            return True
        if col == 0 or (col + 1) == self.col_count:
            return True

        if(self.is_visible_from_left(row, col)):
            return True
        if(self.is_visible_from_right(row, col)):
            return True
        if(self.is_visible_from_top(row, col)):
            return True
        if(self.is_visible_from_bottom(row, col)):
            return True

        return False

    def find_highest_score(self):
        highest_score = 0
        for i in range(0, self.row_count):
            for j in range(0, self.col_count):
                score = self.get_scenic_score(i, j)
                if score > highest_score:
                    highest_score = score
        return highest_score

    def get_scenic_score(self, row, col):
        assert ((row >= 0) and (row < self.row_count) and (col >= 0) and (col < self.col_count))
        
        own_height = int(self.rows[row][col])
        score_left = 0
        for i in range(col - 1, -1, -1):
            score_left += 1
            if int(self.rows[row][i]) >= own_height:
                break
        score_right = 0
        for i in range(col + 1, self.col_count):
            score_right += 1
            if int(self.rows[row][i]) >= own_height:
                break
        score_top = 0
        for i in range(row - 1, -1, -1):
            score_top += 1
            if int(self.rows[i][col]) >= own_height:
                break
        score_bottom = 0
        for i in range(row + 1, self.col_count):
            score_bottom += 1
            if int(self.rows[i][col]) >= own_height:
                break
        return score_left * score_right * score_top * score_bottom

       
def main():
    woods = Woods('input1.txt')
    
    print('# First question')
    print(f'Number of visible trees from outside of grid: {woods.count_visible_trees()}')

    print('# Second question')
    print(f'Highest scenic score: {woods.find_highest_score()}')
   

if __name__ == '__main__':
    main()