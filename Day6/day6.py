""" Advent of Code 2022, Day 6
    Author: Chi-Kit Pao
"""

import os

def find_first_marker(input_file_name: str, marker_length):
    file_path = os.path.dirname(__file__)    
    with open(os.path.join(file_path, input_file_name), 'r') as f:
        rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))
        row = rows[0]
        for i in range(marker_length-1, len(row)):
            if len(set(row[i - marker_length + 1 : i+1])) == marker_length:  # different characters
                print(f"First marker after character {i+1}.")
                return

    print("First marker not found!")


def main():
    print("# First question")
    find_first_marker('input1.txt', 4)
    print("# Second question")
    find_first_marker('input1.txt', 14)


if __name__ == '__main__':
    main()