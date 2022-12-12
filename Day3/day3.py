""" Advent of Code 2022, Day 3
    Author: Chi-Kit Pao
"""

import os


def get_priority(char):
    if ord(char[0]) >= ord('a') and ord(char[0]) <= ord('z'):
        return ord(char[0]) - ord('a') + 1
    elif ord(char[0]) >= ord('A') and ord(char[0]) <= ord('Z'):
        return ord(char[0]) - ord('A') + 27
    else:
        raise ValueError(f"Invalid item {char} is found!")


def calculate_priorities(input_file_name: str):    
    file_path = os.path.dirname(__file__)    
    with open(os.path.join(file_path, input_file_name), 'r') as f:
        rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))

        sum_of_priorites = 0
        for row in rows:
            assert (len(row) % 2 == 0)
            set1 = set(row[0:len(row)//2])
            set2 = set(row[len(row)//2:])
            intersection = set1.intersection(set2)
            assert (len(intersection) == 1)
            (item,) = intersection
            sum_of_priorites += get_priority(item)

        print(f"Sum of priorities: {sum_of_priorites}")


def calculate_priorities_2(input_file_name: str):    
    file_path = os.path.dirname(__file__)    
    with open(os.path.join(file_path, input_file_name), 'r') as f:
        rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))

        sum_of_priorites = 0
        row_count = len(rows)
        for row_index in range(0, row_count, 3):
            if row_index + 2 >= row_count:
                break
            set1 = set(rows[row_index])
            set2 = set(rows[row_index + 1])
            set3 = set(rows[row_index + 2])
            intersection = set1.intersection(set2).intersection(set3)
            assert (len(intersection) == 1)
            (item,) = intersection
            sum_of_priorites += get_priority(item)

        print(f"Sum of priorities: {sum_of_priorites}")


def main():
    calculate_priorities('input1.txt')  # First question
    calculate_priorities_2('input1.txt')  # Second question

if __name__ == '__main__':
    main()