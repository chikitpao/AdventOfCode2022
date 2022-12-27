""" Advent of Code 2022, Day 20
    Author: Chi-Kit Pao
"""


import os

def debug_output(message):
    # print(message)
    pass

class Item:
    def __init__(self, number: int):
        self.number = number

class Quiz:
    def __init__(self, input_file_name: str):
        self.original_list: list[Item] = []
        self.working_list: list[Item] = []
        self.__read_numbers(input_file_name)

    def run(self, decryption=False):
        self.working_list = self.original_list.copy()
        length = len(self.working_list)

        round_count = 1
        if decryption:
            round_count = 10
            for i in range(len(self.working_list)):
                self.working_list[i].number *= 811589153
        for _ in range(round_count):     
            for i in range(len(self.original_list)):
                item = self.original_list[i]
                index = self.working_list.index(item)
                assert index != -1
                if item.number == 0:
                    continue
                new_pos = (index + item.number) % (length - 1)
                # # adjustment for left shift to begin -> move to end
                # # Only to be conform to test example. Doesn't matter at all for 
                # # circular list
                # if new_pos == 0 and self.numbers[i] < 0:
                #     new_pos = length - 1
                self.working_list.insert(new_pos, self.working_list.pop(index))

    def sum(self):
        length = len(self.working_list)
        index_of_0 = next(i for i, item in enumerate(self.working_list) if item.number == 0)
        value_1000th = self.working_list[(index_of_0 + 1000) % length].number
        value_2000th = self.working_list[(index_of_0 + 2000) % length].number
        value_3000th = self.working_list[(index_of_0 + 3000) % length].number
        debug_output(f'value_1000th {value_1000th} value_2000th {value_2000th} value_3000th {value_3000th}')
        return value_1000th + value_2000th + value_3000th


    def __read_numbers(self, input_file_name):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))

        for line in lines:
            if len(line) > 0:
                item = Item(int(line))
                self.original_list.append(item)

def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1

    quiz = Quiz(file_names[file_names_index])
    print('# First question')
    quiz.run(decryption=False)
    print(f'Sum of three number: {quiz.sum()}')

    print('\n# Second question')
    quiz.run(decryption=True)
    print(f'Sum of three number: {quiz.sum()}')

if __name__ == '__main__':
    main()