""" Advent of Code 2022, Day 16, Part 2
    Author: Chi-Kit Pao
"""

import itertools
import os
import copy


def debug_output(message):
    # print(message)
    pass


# from start to useful valve or from useful valve to useful valve
class RouteSegment:
    def __init__(self, start_valve, end_valve, route):
        self.start_valve = start_valve
        self.end_valve = end_valve
        self.route = route  # indices
        self.distance = len(route) - 1

    def __str__(self):
        return f'{self.start_valve.name} to {self.end_valve.name}: {self.route} distance: {self.distance}'


# from start to useful valve or from useful valve to useful valve, might travel over useful valves,
# open the last valve
class RouteSegmentCompound:
    def __init__(self):
        self.route_segments = []
        self.distance = float('inf')
    
    def add_segment(self, segment):
        if len(self.route_segments) == 0:
            self.distance = segment.distance
        else:
            self.distance += segment.distance
        self.route_segments.append(segment)

    def get_duration(self):
        # + 1 for opening valve
        return self.distance if self.distance == 0 else (self.distance + 1)

    # def __str__(self):
    #    temp_str = ''
    #    for i, segment in enumerate(self.route_segments):
    #        temp_str += str(segment)
    #        if i + 1 < len(self.route_segments):
    #            temp_str += ', '
    #    return f'[{temp_str}] distance: {self.distance}'
    def __str__(self):
        temp_str = ''
        for i, segment in enumerate(self.route_segments):
            temp_str += segment.start_valve.name + '->' + segment.end_valve.name
            if i + 1 < len(self.route_segments):
                temp_str += ', '
        return f'{temp_str} duration {self.get_duration()} distance: {self.distance}'


# Compound of RouteSegmentCompound
class RouteSegmentCompoundCompound:
    def __init__(self, maximum_duration):
        self.route_segment_compounds = []
        self.distance = 0
        self.maximum_duration = maximum_duration

    def add_compound(self, compound):
        self.route_segment_compounds.append(compound)
        self.distance += compound.distance

    def calculate_pressure(self, debug=False):
        total_pressure = 0
        total_duration = 0
        for compound in self.route_segment_compounds:
            duration = compound.get_duration()
            if debug:
                print(f'duration: {duration}')
            total_duration += duration
            if debug:
                print(f'valve: {compound.route_segments[-1].end_valve.name} rate: {compound.route_segments[-1].end_valve.rate}')
            pressure = compound.route_segments[-1].end_valve.rate * (self.maximum_duration - total_duration)
            if debug:
                print(f'pressure: {pressure}')
            total_pressure += pressure
        return total_pressure
    
    def get_detail_route_description(self, volcano):
        temp_str = ''
        for compound in self.route_segment_compounds:
            for segment in compound.route_segments:
                named_segment = list(map(lambda i: volcano.valves[i].name, segment.route))
                temp_str += str(named_segment) + ', '
            temp_str += 'open\n'
        return temp_str

    def get_duration(self):
        return self.distance + len(self.route_segment_compounds)
    
    def remove_last_compound(self):
        self.distance -= self.route_segment_compounds[-1].distance
        self.route_segment_compounds.pop()

    def __str__(self):
        temp_str = ''
        for i, compound in enumerate(self.route_segment_compounds):
            temp_str += compound.route_segments[0].start_valve.name + '->' + compound.route_segments[-1].end_valve.name
            if i + 1 < len(self.route_segment_compounds):
                temp_str += ', '
        return f'RouteSegmentCompoundCompound: duration {self.get_duration()}, pressure {self.calculate_pressure()} {temp_str}'


class Valve:
    def __init__(self, name, rate, neighbors):
        self.name = name
        self.rate = rate
        # names at initialization, indices after __replace_neighbor_names_by_indices
        self.neighbors = neighbors  
        self.index = -1
        # only filled for start valve and for useful valves
        self.routes_to_useful_valves = []

class TestRouteData:
    def __init__(self, start_valve_index, maximum_duration):
        self.corner_points_set = {start_valve_index}
        self.corner_points_bits = 1 << start_valve_index
        self.corner_points_bits = 1 << start_valve_index
        self.route_segment_compound_compound_dict = {}
        self.route_segment_compound_compound = RouteSegmentCompoundCompound(maximum_duration)
        self.best_pressure = None
        self.best_route0 = None
        self.best_route1 = None


class Volcano:
    def __init__(self, input_file_name: str):
        self.valves_lookup = {}  # name -> valve 
        self.valves = None  # List of valves
        self.useful_valves_count = 0
        self.distance_matrix = None
        self.maximum_duration = 26

        self.__read_in_valves(input_file_name)
        debug_output(f'useful_valves_count: {self.useful_valves_count}')
        self.__assign_valve_indices()
        self.__replace_neighbor_names_by_indices()

        # Simplification: We always start at non-functioning valve
        self.start_valve = self.valves_lookup['AA']
        assert self.start_valve.rate == 0
        
        self.start_valve.routes_to_useful_valves = self.find_routes_bfs_from(self.start_valve)

        for i in range(self.useful_valves_count):
            self.valves[i].routes_to_useful_valves = self.find_routes_bfs_from(self.valves[i])

        self.create_distance_matrix()
    
    def create_distance_matrix(self):
        self.distance_matrix = []
        #  Use Floyd–Warshall algorithm here
        for i in range(self.useful_valves_count + 1):
            rsc = []
            for j in range(self.useful_valves_count + 1):
                rsc.append(RouteSegmentCompound())
            self.distance_matrix.append(rsc)
            self.distance_matrix[i][i].distance = 0
        self.insert_valve_routes_into_distance_matrix(self.start_valve, self.useful_valves_count)
        for i in range(self.useful_valves_count):
            self.insert_valve_routes_into_distance_matrix(self.valves[i], i)

        for k in range(self.useful_valves_count + 1):
            for i in range(self.useful_valves_count + 1):
                for j in range(self.useful_valves_count + 1):
                    if self.distance_matrix[i][j].distance > self.distance_matrix[i][k].distance + self.distance_matrix[k][j].distance:
                        self.distance_matrix[i][j].route_segments = self.distance_matrix[i][k].route_segments + self.distance_matrix[k][j].route_segments 
                        self.distance_matrix[i][j].distance = self.distance_matrix[i][k].distance + self.distance_matrix[k][j].distance

        for i in range(self.useful_valves_count + 1):
            for j in range(self.useful_valves_count + 1):
                debug_output(f'{i}, {j}, {self.distance_matrix[i][j]}')

    def insert_valve_routes_into_distance_matrix(self, valve, index):
        for r in valve.routes_to_useful_valves:
            self.distance_matrix[index][r.end_valve.index].add_segment(r)

    def find_routes_bfs_from(self, start_valve):
        visited = [None] * len(self.valves)
        candidates = [start_valve.index]
        while len(candidates) > 0:
            current_valve = self.valves[candidates.pop(0)]
            for n in current_valve.neighbors:
                if self.valves[n] == start_valve:
                    continue
                if visited[n] is not None:
                    continue
                visited[n] = current_valve.index
                # Don't traverse over useful valves
                if self.valves[n].rate > 0:
                    continue
                candidates.append(n)

        routes_from_start = []
        for i in range(self.useful_valves_count):
            route = []
            ii = i
            while visited[ii] is not None:
                route.insert(0, ii)
                ii = visited[ii]
            if len(route) > 0:
                route.insert(0, start_valve.index)
                routes_from_start.append(RouteSegment(start_valve, self.valves[i], route))
                debug_output(str(routes_from_start[-1]) + ' ' + str(list(map(lambda v: self.valves[v].name, route))))
        return routes_from_start

    def test_routes(self, current_valve, test_route_data):
        # Use backtracking to iterate all possible solutions
        for i in range(self.useful_valves_count):
            if i in test_route_data.corner_points_set:
                continue

            test_route_data.corner_points_set.add(i)
            test_route_data.corner_points_bits |= 1 << i
            if current_valve == self.start_valve:
                compound = self.distance_matrix[self.useful_valves_count][i]
            else:
                compound = self.distance_matrix[current_valve.index][i]
            test_route_data.route_segment_compound_compound.add_compound(compound)
            duration = test_route_data.route_segment_compound_compound.get_duration()
            if(duration < self.maximum_duration):
                # debug_output(f'test_routes: {test_route_data.route_segment_compound_compound}')
                pressure = test_route_data.route_segment_compound_compound.calculate_pressure()

                if test_route_data.corner_points_bits not in test_route_data.route_segment_compound_compound_dict \
                    or test_route_data.route_segment_compound_compound_dict[test_route_data.corner_points_bits][1] < pressure:
                    test_route_data.route_segment_compound_compound_dict[test_route_data.corner_points_bits] = \
                        (copy.deepcopy(test_route_data.route_segment_compound_compound), pressure)
                self.test_routes(self.valves[i], test_route_data)
            test_route_data.route_segment_compound_compound.remove_last_compound()
            test_route_data.corner_points_set.remove(i)
            test_route_data.corner_points_bits &= ~(1 << i)

    def __assign_valve_indices(self):
        # Assign indices to valves, useful valves have lowest indices
        self.valves = [None] * len(self.valves_lookup)
        useful_valves_index = 0
        useless_valves_index = self.useful_valves_count
        for valve in self.valves_lookup.values():
            if valve.rate > 0:
                valve.index = useful_valves_index
                self.valves[useful_valves_index] = valve
                useful_valves_index += 1
            else:
                valve.index = useless_valves_index
                self.valves[useless_valves_index] = valve
                useless_valves_index += 1

    def __read_in_valves(self, input_file_name):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            for line in lines:
                # Line example: 'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB'
                # Relevant information at indices 1, 4, 9 ff.
                tokens = line.split()
                name = tokens[1]
                rate = int(tokens[4].replace(';', '').split('=')[1])
                if rate > 0:
                    self.useful_valves_count += 1
                neighbors = []
                for i in range(9, len(tokens)):
                    neighbors.append(tokens[i].replace(',', ''))
                valve = Valve(name, rate, neighbors)
                self.valves_lookup[valve.name] = valve

    def __replace_neighbor_names_by_indices(self):
        for v in self.valves:
            indices = list(map(lambda n: self.valves_lookup[n].index, v.neighbors))
            v.neighbors = indices
        

def main():
    # volcano = Volcano('test.txt')
    volcano = Volcano('input1.txt')

    print('# Second question')
    test_route_data = TestRouteData(volcano.start_valve.index, volcano.maximum_duration)
    volcano.test_routes(volcano.start_valve, test_route_data)
    start_valve_bit = 1 << volcano.start_valve.index
    for pair in itertools.product(test_route_data.route_segment_compound_compound_dict.keys(), test_route_data.route_segment_compound_compound_dict.keys()):
        if pair[0] < pair[1] and (pair[0] & pair[1] == start_valve_bit):  # Test disjunct valves on both routes
            item0 = test_route_data.route_segment_compound_compound_dict[pair[0]]
            item1 = test_route_data.route_segment_compound_compound_dict[pair[1]]
            if test_route_data.best_pressure is None or test_route_data.best_pressure < item0[1] + item1[1]:
                test_route_data.best_pressure = item0[1] + item1[1]
                test_route_data.best_route0 = item0[0]
                test_route_data.best_route1 = item1[0]
    assert (test_route_data.best_route0 is not None and test_route_data.best_route0 is not None)
    print('Total pressure:', test_route_data.best_pressure)
    print(test_route_data.best_route0)
    print(test_route_data.best_route0.get_detail_route_description(volcano))
    print(test_route_data.best_route1)
    print(test_route_data.best_route1.get_detail_route_description(volcano))
    test_route_data.best_route0.calculate_pressure(debug=True)
    print('')
    test_route_data.best_route1.calculate_pressure(debug=True)


if __name__ == '__main__':
    main()