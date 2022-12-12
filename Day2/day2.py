""" Advent of Code 2022, Day 2
    Author: Chi-Kit Pao
"""

import os

def get_score(opponent_char, own_char):
    # Rock = 0, Paper = 1, Scissors = 2
    opponent_choice = ord(opponent_char) - ord('A')
    own_choice = ord(own_char) - ord('X')
    
    score_by_choice = own_choice + 1
    score_by_result = 3  # Default: draw
    if opponent_choice == own_choice:
        return score_by_choice + score_by_result

    if ((opponent_choice + 1) % 3) == own_choice:
        return score_by_choice + 6  # I've won.

    return score_by_choice  # I've lost.


def calculate_scores(input_file_name: str, question: int):
    assert question in [1, 2]

    scores = []
    
    file_path = os.path.dirname(__file__)    
    with open(os.path.join(file_path, input_file_name), 'r') as f:
        rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))

        for row in rows:
            if len(row) >= 3:
                if question == 1:
                    scores.append(get_score(row[0], row[2]))
                else:
                    opponent_choice = ord(row[0]) - ord('A')
                    own_choice = opponent_choice  # Default: draw
                    if row[2] == 'X':  # I have to lose
                        own_choice = (opponent_choice - 1) if (opponent_choice > 0) else 2
                    elif row[2] == 'Z':  # I have to win
                        own_choice = (opponent_choice + 1) % 3
                    scores.append(get_score(row[0], chr(ord('X') + own_choice)))

    # print(f"Scores: {scores}")
    print(f"Total scores: {sum(scores)}")


def main():
    calculate_scores('input1.txt', 1)  # First question
    calculate_scores('input1.txt', 2)  # Second question


if __name__ == '__main__':
    main()