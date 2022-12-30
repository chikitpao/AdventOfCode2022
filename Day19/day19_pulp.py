""" Advent of Code 2022, Day 19
    Author: Chi-Kit Pao
    REMARK: Requires library PuLP to run this program.
"""


import os
import pulp as plp
import time

def debug_output(message):
    # print(message)
    pass

class Blueprint:
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3
    MAX_TYPES = 4
    
    def __init__(self, number):
        self.number = number
        self.robot_instructions = [None] * Blueprint.MAX_TYPES
        self.name_templates = ['{}_ore', '{}_clay', '{}_obsidian', '{}_geode']
        self.robot_names = []
        # Total number of robots per round
        self.robots = []
        self.resource_names = []
        # Total number of resources per round
        self.resources = []
        self.build_names = []
        # Number of builds in a single round
        self.builds = []
        for i in range(Blueprint.MAX_TYPES):
            self.robot_names.append(self.name_templates[i].format('robots'))
            self.resource_names.append(self.name_templates[i].format('resources'))
            self.build_names.append(self.name_templates[i].format('builds'))

    def add_robot_instruction(self, robot_type, costs):
        self.robot_instructions[robot_type] = costs

    def run(self, minutes):
        self.robots.clear()
        self.resources.clear()
        self.builds.clear()
        for i in range(Blueprint.MAX_TYPES):
            self.robots.append([])
            self.resources.append([])
            self.builds.append([])

        problem = plp.LpProblem(f'Blueprint{self.number:02d}', plp.LpMaximize)
        for i in range(minutes):
           self.robots[Blueprint.GEODE].append(plp.LpVariable(f'{self.robot_names[Blueprint.GEODE]}{i:02d}', 0, 0 if i == 0 else None, plp.LpInteger))
        # Find maximum sum of total numbers of geode of all rounds -> number of geodes opened.
        problem += sum(self.robots[Blueprint.GEODE])
        for i in range(minutes):
            for j in range(Blueprint.GEODE):  # everything except Geode
                if i == 0:
                    min_max = (1, 1) if j == Blueprint.ORE else (0, 0)
                    self.robots[j].append(plp.LpVariable(f'{self.robot_names[j]}{i:02d}', min_max[0], min_max[1], plp.LpInteger))
                    self.resources[j].append(plp.LpVariable(f'{self.resource_names[j]}{i:02d}', 0, 0, plp.LpInteger))
                else:
                    self.robots[j].append(plp.LpVariable(f'{self.robot_names[j]}{i:02d}', 0, None, plp.LpInteger))
                    self.resources[j].append(plp.LpVariable(f'{self.resource_names[j]}{i:02d}', 0, None, plp.LpInteger))
                self.builds[j].append(plp.LpVariable(f'{self.build_names[j]}{i:02d}', 0, 1, plp.LpInteger))
            self.builds[Blueprint.GEODE].append(plp.LpVariable(f'{self.build_names[Blueprint.GEODE]}{i:02d}', 0, 1, plp.LpInteger))
            
            # Constraint: Maximum one robot build per round
            problem += self.builds[Blueprint.ORE][-1] + self.builds[Blueprint.CLAY][-1] + self.builds[Blueprint.OBSIDIAN][-1] + self.builds[Blueprint.GEODE][-1] <= 1

            if i == 0:
                continue

            # Constraints for modelling available resources
            problem += self.resources[Blueprint.ORE][-1] == self.resources[Blueprint.ORE][-2] + self.robots[Blueprint.ORE][-2] \
                - self.builds[Blueprint.ORE][-1] * self.robot_instructions[Blueprint.ORE][Blueprint.ORE] \
                - self.builds[Blueprint.CLAY][-1] * self.robot_instructions[Blueprint.CLAY][Blueprint.ORE] \
                - self.builds[Blueprint.OBSIDIAN][-1] * self.robot_instructions[Blueprint.OBSIDIAN][Blueprint.ORE] \
                - self.builds[Blueprint.GEODE][-1] * self.robot_instructions[Blueprint.GEODE][Blueprint.ORE]
            problem += self.resources[Blueprint.CLAY][-1] == self.resources[Blueprint.CLAY][-2] + self.robots[Blueprint.CLAY][-2] \
                - self.builds[Blueprint.OBSIDIAN][-1] * self.robot_instructions[Blueprint.OBSIDIAN][Blueprint.CLAY]
            problem += self.resources[Blueprint.OBSIDIAN][-1] == self.resources[Blueprint.OBSIDIAN][-2] + self.robots[Blueprint.OBSIDIAN][-2] \
                - self.builds[Blueprint.GEODE][-1] * self.robot_instructions[Blueprint.GEODE][Blueprint.OBSIDIAN]
            # Constraints: Build only possible if resources are available.
            problem += self.resources[Blueprint.ORE][-2] - self.builds[Blueprint.ORE][-1] * self.robot_instructions[Blueprint.ORE][Blueprint.ORE] >= 0
            problem += self.resources[Blueprint.ORE][-2] - self.builds[Blueprint.CLAY][-1] * self.robot_instructions[Blueprint.CLAY][Blueprint.ORE] >= 0
            problem += self.resources[Blueprint.ORE][-2] - self.builds[Blueprint.OBSIDIAN][-1] * self.robot_instructions[Blueprint.OBSIDIAN][Blueprint.ORE] >= 0
            problem += self.resources[Blueprint.ORE][-2] - self.builds[Blueprint.GEODE][-1] * self.robot_instructions[Blueprint.GEODE][Blueprint.ORE] >= 0
            problem += self.resources[Blueprint.CLAY][-2] - self.builds[Blueprint.OBSIDIAN][-1] * self.robot_instructions[Blueprint.OBSIDIAN][Blueprint.CLAY] >= 0
            problem += self.resources[Blueprint.OBSIDIAN][-2] - self.builds[Blueprint.GEODE][-1] * self.robot_instructions[Blueprint.GEODE][Blueprint.OBSIDIAN] >= 0
            # Constraints for modelling robot builds
            for j in range(Blueprint.GEODE):  # everything except Geode
                problem += self.robots[j][-1] == self.robots[j][-2] + self.builds[j][-1]
            problem += self.robots[Blueprint.GEODE][i] == self.robots[Blueprint.GEODE][i - 1] + self.builds[Blueprint.GEODE][-1]

        print(problem)
        status = problem.solve()
        debug_output(f'status: {status}')
        debug_output(f'problem.objective.value() {problem.objective.value()}')
        return problem.objective.value()


class Quiz:
    def __init__(self, input_file_name: str):
        self.blue_prints = []
        self.__read_blueprint(input_file_name)

    def __read_blueprint(self, input_file_name):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            for line in lines:
                # Example text: 'Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 3 ore and 13 obsidian.'
                assert line.find('Blueprint') != -1
                str_blue_print, str_after_blue_print = line.split(':')
                str_dummy, str_blue_print_no = str_blue_print.split()
                blueprint = Blueprint(int(str_blue_print_no))
                self.blue_prints.append(blueprint)
                for robot_instruction in str_after_blue_print.strip().split('.'):
                    robot_instruction_tokens = robot_instruction.split()
                    if len(robot_instruction_tokens) == 0:
                        continue
                    if robot_instruction_tokens[1] == 'ore':
                        assert len(robot_instruction_tokens) == 6 and robot_instruction_tokens[5] == 'ore'
                        blueprint.add_robot_instruction(Blueprint.ORE, {Blueprint.ORE: int(robot_instruction_tokens[4])})
                    elif robot_instruction_tokens[1] == 'clay':
                        assert len(robot_instruction_tokens) == 6 and robot_instruction_tokens[5] == 'ore'
                        blueprint.add_robot_instruction(Blueprint.CLAY, {Blueprint.ORE: int(robot_instruction_tokens[4])})
                    if robot_instruction_tokens[1] == 'obsidian':
                        assert len(robot_instruction_tokens) == 9 and robot_instruction_tokens[5] == 'ore' and robot_instruction_tokens[8] == 'clay'
                        blueprint.add_robot_instruction(Blueprint.OBSIDIAN, {Blueprint.ORE: int(robot_instruction_tokens[4]), Blueprint.CLAY: int(robot_instruction_tokens[7])})
                    elif robot_instruction_tokens[1] == 'geode':
                        assert len(robot_instruction_tokens) == 9 and robot_instruction_tokens[5] == 'ore' and robot_instruction_tokens[8] == 'obsidian'
                        blueprint.add_robot_instruction(Blueprint.GEODE, {Blueprint.ORE: int(robot_instruction_tokens[4]), Blueprint.OBSIDIAN: int(robot_instruction_tokens[7])})


def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1

    quiz = Quiz(file_names[file_names_index])
    
    start_time = time.time()
    # First question
    total_quality_level = 0
    for bp in quiz.blue_prints:
        quality_level = bp.run(24)
        total_quality_level += bp.number * quality_level
        debug_output(f' number: {bp.number}, quality_level: {quality_level}, product {bp.number * quality_level}')
    print('# First question')
    print(f'Quality level: {total_quality_level}')


    # Second question
    result = 1
    for bp in quiz.blue_prints[:3]:
        quality_level = bp.run(32)
        result *= quality_level
    print('# Second question')
    print(f'Result: {result}')
    print(f'Time elapsed: {time.time() - start_time} s')


if __name__ == '__main__':
    main()
