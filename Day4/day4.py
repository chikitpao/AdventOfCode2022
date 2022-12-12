""" Advent of Code 2022, Day 4
    Author: Chi-Kit Pao
"""

import os


def contains_fully(lhs, rhs):
    if rhs[0] >= lhs[0] and rhs[1] <= lhs[1]:
        return True
    return False


def overlapped(lhs, rhs):
    # rhs begin in lhs
    if rhs[0] >= lhs[0] and rhs[0] <= lhs[1]:
        return True
    # rhs end in lhs
    if rhs[1] >= lhs[0] and rhs[1] <= lhs[1]:
        return True
    # lhs begin in rhs
    if lhs[0] >= rhs[0] and lhs[0] <= rhs[1]:
        return True
    # lhs end in rhs
    if lhs[1] >= rhs[0] and lhs[1] <= rhs[1]:
        return True

    return False


def check_assignment(input_file_name: str, question: int):
    assert (question in [1, 2])
    file_path = os.path.dirname(__file__)    
    with open(os.path.join(file_path, input_file_name), 'r') as f:
        count = 0

        rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))
        for row in rows:
            columns = row.split(',')
            if len(columns) < 2:
                break
            assert (len(columns) == 2)
            lhs = list(map(lambda s: int(s), columns[0].split('-')))
            rhs = list(map(lambda s: int(s), columns[1].split('-')))
            if question == 1:
                if contains_fully(lhs, rhs) or contains_fully(rhs, lhs):
                    count += 1
            else:
                if overlapped(lhs, rhs):
                    count += 1
        
        if question == 1:
            print(f"Pairs with fully containment: {count}")
        else:
            print(f"Pairs with overlapping assigment: {count}")


def main():
    check_assignment('input1.txt', 1)  # First question
    check_assignment('input1.txt', 2)  # Second question

if __name__ == '__main__':
    main()