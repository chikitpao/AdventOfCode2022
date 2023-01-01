""" Advent of Code 2022, Day 25
    Author: Chi-Kit Pao
"""


import os


def debug_output(message):
    # print(message)
    pass

def snafu_to_decimal(snafu: str) -> int:
    translation = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
    result = 0
    unit = 1
    for i in range(len(snafu) - 1, -1, -1):
        result += translation[snafu[i]] * unit
        unit *= 5
    return result

def decimal_to_snafu(dec: int) -> str:
    if dec == 0:
        return '0'
    
    translation = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-'}
    result_list = []
    dividend = dec
    while dividend != 0:
        remainder = dividend % 5
        dividend = dividend // 5
        result_list.insert(0, translation[remainder])
        if remainder >= 3:
            dividend += 1        
    return ''.join(result_list)

def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1

    lines = None
    file_path = os.path.dirname(__file__)
    with open(os.path.join(file_path, file_names[file_names_index]), 'r') as f:
        lines = list(map(lambda s: s.replace('\n', ''), f.readlines()))

    print('# First question')
    sum_decimal = 0
    for line in lines:
        sum_decimal += snafu_to_decimal(line)
    sum_snafu = decimal_to_snafu(sum_decimal)
    print(f'Result: {sum_snafu}')


if __name__ == '__main__':
    main()