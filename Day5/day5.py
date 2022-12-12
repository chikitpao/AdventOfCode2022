""" Advent of Code 2022, Day 5
    Author: Chi-Kit Pao
"""

import os

def move_stack_1(stacks, item_count, from_index, to_index):
    for i in range(0, item_count):
        stacks[to_index].append(stacks[from_index].pop())


def move_stack_2(stacks, item_count, from_index, to_index):
    temp_stack = []
    for i in range(0, item_count):
        temp_stack.insert(0, stacks[from_index].pop())
    stacks[to_index].extend(temp_stack)


def operate_on_stacks(input_file_name: str, move_stack_func):
    file_path = os.path.dirname(__file__)    
    with open(os.path.join(file_path, input_file_name), 'r') as f:
        rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))
        
        # Initialize stack 
        stacks = {}
        for i in range(1, 10):
            stacks[i] = []
        for row in rows[0: 8]:
            for j in range(0, len(row)):
                if row[j] == '[':
                    stacks[j // 4 + 1].insert(0, row[j+1])  # insert item to the front
        
        print("stacks before: ", stacks)

        for row in rows[10:]:
            # e.g. "move 3 from 3 to 7"
            columns = row.split()
            assert (columns[0] == 'move' and columns[2] == 'from' and columns[4] == 'to')
            item_count = int(columns[1])
            from_index = int(columns[3])
            to_index = int(columns[5])
            move_stack_func(stacks, item_count, from_index, to_index)

        print("stacks after: ", stacks)

        result = []
        for i in range(1, 10):
            result.append(stacks[i][-1])
        print("result: ", result)


def main():
    print("# First question")
    operate_on_stacks('input1.txt', move_stack_1)  # First question
    print("# Second question")
    operate_on_stacks('input1.txt', move_stack_2)  # Second question


if __name__ == '__main__':
    main()