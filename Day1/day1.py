""" Advent of Code 2022, Day 1
    Author: Chi-Kit Pao
"""

import os

def calculate_calories(input_file_name: str):
    intakes = []
    
    file_path = os.path.dirname(__file__)    
    with open(os.path.join(file_path, input_file_name), 'r') as f:
        rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))

        calories_sum = None
        for row in rows:
            if len(row.strip()) == 0:
                if calories_sum is not None:
                    intakes.append(calories_sum)
                    calories_sum = None
            else:
                calories = int(row)
                if calories_sum is None:
                    calories_sum = calories
                else:
                    calories_sum += calories
        
        # EOF without blank line -> Store last sum if it exists.
        if calories_sum is not None:
            intakes.append(calories_sum)

    # print(f"Calories intakes: {intakes}")
    print(f"Maximum calories intake: {max(intakes)}")  # First answer

    intakes.sort(reverse=True)  # Sort in descending order
    print(f"Sum of top 3 calories intakes: {sum(intakes[0:3])}")  # Second answer


def main():
    calculate_calories('input1.txt')


if __name__ == '__main__':
    main()