""" Advent of Code 2022, Day 11
    Author: Chi-Kit Pao
"""

import os

def debug_output(message):
    #print(message)
    pass


class Monkey:
    def __init__(self, id):
        self.id = id
        self.items = []
        self.operation = None
        self.divisor = None
        self.true_monkey = None
        self.false_monkey = None
        self.inspection_count = 0
        self.relief = False
        self.common_divisor = None # For manageable worry levels

    def __str__(self):
        return str(self.id) + " " + str(self.items)

    def inspect_item(self):
        self.inspection_count += 1
        item = self.items.pop(0)
        debug_output(f'  Monkey inspects an item with a worry level of {item}.')
        item = self.operation(item)
        debug_output(f'    Worry level changes to {item}.')
        if self.relief:
            item = item // 3
        else:
            item = item % self.common_divisor
        debug_output(f'    Monkey gets bored with item. Worry level is divided by 3 to {item}.')
        if item % self.divisor == 0:
            debug_output(f'    Test returned true. Item with worry level {item} is thrown to monkey {self.true_monkey}.')
            return self.true_monkey, item
        else:
            debug_output(f'    Test returned false. Item with worry level {item} is thrown to monkey {self.false_monkey}.')
            return self.false_monkey, item

    def add_item(self, item):
        self.items.append(item)


class MonkeyBusiness:
    def __init__(self, input_file_name: str, relief: bool):
        self.lines = []
        self.monkeys = {}
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            self.lines = list(map(lambda s: s.replace('\n', ''), f.readlines()))

        i = 0
        common_divisor = 1
        while i < len(self.lines):
            # line 0: Monkey 0:
            line0 = self.lines[i + 0].split()  
            monkey = Monkey(int(line0[1][:-1]))
            # line 1:   Starting items: 79, 98
            remaining = self.consume_text(self.lines[i + 1], 'Starting items:')
            monkey.items = list(map(lambda s: int(s), remaining.split(',')))
            ## line 2:   Operation: new = old * 19
            #remaining = self.consume_text(self.lines[i + 2], 'Operation: new = old *')   
            #monkey.operation = lambda x: x * int(remaining)
            # line 3:   Test: divisible by 23
            remaining = self.consume_text(self.lines[i + 3], 'Test: divisible by')
            monkey.divisor = int(remaining)
            # line 4:     If true: throw to monkey 2
            remaining = self.consume_text(self.lines[i + 4], 'If true: throw to monkey')
            monkey.true_monkey = int(remaining)
            # line 5:     If false: throw to monkey 3 
            remaining = self.consume_text(self.lines[i + 5], 'If false: throw to monkey')
            monkey.false_monkey = int(remaining)
            monkey.relief = relief
            if not relief:
                common_divisor *= monkey.divisor
            self.monkeys[monkey.id] = monkey
            i += 7
        
        if not relief:
            for monkey in self.monkeys.values():
                monkey.common_divisor = common_divisor

    def add_operation(self, monkey_id, func):
        self.monkeys[monkey_id].operation = func

    def add_test_operations(self):
        self.add_operation(0, lambda x: x * 19)
        self.add_operation(1, lambda x: x + 6)
        self.add_operation(2, lambda x: x * x)
        self.add_operation(3, lambda x: x + 3)

    def add_part1_operations(self):
        self.add_operation(0, lambda x: x * 7)
        self.add_operation(1, lambda x: x * 11)
        self.add_operation(2, lambda x: x + 8)
        self.add_operation(3, lambda x: x + 7)
        self.add_operation(4, lambda x: x + 5)
        self.add_operation(5, lambda x: x + 4)
        self.add_operation(6, lambda x: x * x)
        self.add_operation(7, lambda x: x + 3)

    def consume_text(self, string, substring):
        index = string.find(substring)
        if index == -1:
            return ""
        return string[index + len(substring):]

    def execute_round(self):
        for monkey in self.monkeys.values():
            debug_output(f'Monkey {monkey.id}')
            while len(monkey.items) > 0:
               new_monkey, item = monkey.inspect_item()
               self.monkeys[new_monkey].add_item(item)
    
    def execute_rounds(self, rounds):
        for i in range(rounds):
            debug_output(f'Round {i + 1}')
            self.execute_round()
        inspection_counts = []
        for monkey in self.monkeys.values():
            debug_output(monkey.inspection_count)
            inspection_counts.append(monkey.inspection_count)
        inspection_counts.sort(reverse=True)
        print(f"Level of monkey business: {inspection_counts[0] * inspection_counts[1]}")

def main():
    print('# First question')
    business = MonkeyBusiness('input1.txt', True)
    #business.add_test_operations()
    business.add_part1_operations()
    business.execute_rounds(20)  
    
    print('# Second question')
    business = MonkeyBusiness('input1.txt', False)
    #business.add_test_operations()
    business.add_part1_operations()
    business.execute_rounds(10000)
   

if __name__ == '__main__':
    main()