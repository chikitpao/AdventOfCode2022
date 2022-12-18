""" Advent of Code 2022, Day 15, Part 2
    Author: Chi-Kit Pao
"""


import os


def debug_output(message):
    # print(message)
    pass

class Sensor:
    def __init__(self, x_sensor, y_sensor, x_beacon, y_beacon):
        self.x_sensor = x_sensor
        self.y_sensor = y_sensor
        # closest beacon
        self.x_beacon = x_beacon
        self.y_beacon = y_beacon
        # Manhattan distance
        self.distance = abs(x_beacon - x_sensor) + abs(y_beacon - y_sensor)

    # returns list with coverage start and (inclusive) end, None if no coverage
    def coverage_at_line(self, line_number):
        if line_number < self.y_sensor - self.distance or line_number > self.y_sensor + self.distance:
            return None

        radius = self.distance - abs(line_number - self.y_sensor)
        start = self.x_sensor - radius
        end = self.x_sensor + radius
        coverage = end - start + 1
        return [start, end]

class BeaconZone:
    def __init__(self, input_file_name: str):
        self.sensors = []
        self.beacons = set()  # known beacons

        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            for line in lines:
                # Line example: 'Sensor at x=3391837, y=2528277: closest beacon is at x=3448416, y=2478759'
                # Relevant information at indices 2, 3, 8, 9
                tokens = line.split()
                x_sensor = int(tokens[2].replace(',', '').split('=')[1])
                y_sensor = int(tokens[3].replace(':', '').split('=')[1])
                x_beacon = int(tokens[8].replace(',', '').split('=')[1])
                y_beacon = int(tokens[9].split('=')[1])
                self.sensors.append(Sensor(x_sensor, y_sensor, x_beacon, y_beacon))
                self.beacons.add((x_beacon, y_beacon))
    
    def debug_total_coverage_range(self, coverage_range, total_coverage_range, line_number):
        if line_number == 2414995 and False:
            debug_output(f'coverage_range: {coverage_range}, total_coverage_range: {total_coverage_range}')

    def find_undetected_beacon(self, xy_min, xy_max):
        for i in range(xy_min, xy_max + 1):
            beacon = self.find_undetected_beacon_at_line(i, xy_min, xy_max)
            if beacon is not None:
                return beacon

        raise ValueError('Cannot find beacon!')

    def find_undetected_beacon_at_line(self, line_number, xy_min, xy_max):
        # total_coverage_range: List of non-overlapping coverage ranges, None if empty
        total_coverage_range = None
        coverage_ranges = []

        for sensor in self.sensors:
            coverage_range = sensor.coverage_at_line(line_number)
            coverage_range = self.truncate_range(coverage_range, xy_min, xy_max)
            if coverage_range is not None:
                coverage_ranges.append(coverage_range)
            if sensor.y_sensor == line_number and sensor.x_sensor >= xy_min and sensor.y_sensor <= xy_max:
                    coverage_ranges.append([sensor.x_sensor, sensor.x_sensor])

        for beacon in self.beacons:
                if beacon[1] == line_number and beacon[0] >= xy_min and beacon[0] <= xy_max:
                    coverage_ranges.append([beacon[0], beacon[0]])
        
        for coverage_range in coverage_ranges:
            if total_coverage_range is None:
                total_coverage_range = []
                total_coverage_range.append(coverage_range)
                self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)
                continue
            
            # Process from the end of list, extend total_coverage_range[] if necessary
            i = len(total_coverage_range) - 1
            while i >= 0:
                if i == len(total_coverage_range) - 1:
                    if coverage_range[0] > total_coverage_range[i][1] + 1:
                        # New coverage range is behind the last existing coverage range and 
                        # cannot be merged to this range -> Append new range
                        total_coverage_range.append(coverage_range)
                        self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)
                    elif coverage_range[1] > total_coverage_range[i][1]:
                        # New coverage range is behind the last existing coverage range and 
                        # can be merged to this range -> Extend end of total_coverage_range[i][1]
                        total_coverage_range[i][1] = coverage_range[1]
                        self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)
                else:
                    if coverage_range[0] > total_coverage_range[i][1] + 1 and coverage_range[1] < total_coverage_range[i + 1][0] - 1:
                        # New coverage range is between current and next existing coverage ranges and 
                        # cannot be merged -> Insert new range
                        total_coverage_range.insert(i + 1, coverage_range)
                        self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)
                    else:
                        if coverage_range[1] >= total_coverage_range[i + 1][0] - 1:
                            if coverage_range[0] > total_coverage_range[i][1] + 1:
                                if coverage_range[0] < total_coverage_range[i + 1][0]:
                                    # Merge next range with new range
                                    total_coverage_range[i + 1][0] = coverage_range[0]
                                    self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)
                            else:
                                # Merge next range with current range
                                total_coverage_range[i][1] = total_coverage_range[i + 1][1]
                                total_coverage_range.pop(i + 1)
                                self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)
                        elif coverage_range[1] >= total_coverage_range[i][1] + 1 and coverage_range[0] <= total_coverage_range[i][1]:
                            # Merge current range with new range
                            total_coverage_range[i][1] = coverage_range[1]
                            self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)

                if i == 0:
                    if coverage_range[1] < total_coverage_range[i][0] - 1:
                        # New coverage range is in front of the first existing coverage range and 
                        # cannot be merged to this range -> Insert new range to the front
                        total_coverage_range.insert(0, coverage_range)
                        self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)
                    elif coverage_range[1] >= total_coverage_range[i][0]:
                        if coverage_range[0] < total_coverage_range[i][0]:
                            # New coverage range is in front the first existing coverage range and 
                            # can be merged to this range -> Extend start of total_coverage_range[i][1]
                            total_coverage_range[i][0] = coverage_range[0]
                            self.debug_total_coverage_range(coverage_range, total_coverage_range, line_number)
                i -= 1

        if total_coverage_range is None:
            return None
        
        if len(total_coverage_range) == 2:
            assert total_coverage_range[0][0] == xy_min and total_coverage_range[1][1] == xy_max
            if total_coverage_range[1][0] - total_coverage_range[0][1] == 2:
                return (total_coverage_range[0][1] + 1, line_number)
        elif len(total_coverage_range) == 1:
            if total_coverage_range[0][0] == 0 and total_coverage_range[0][1] == xy_max - 1:
                return (xy_max, line_number)
            elif total_coverage_range[0][0] == 1 and total_coverage_range[0][1] == xy_max:
                return (0, line_number)
            elif total_coverage_range[0][0] == 0 and total_coverage_range[0][1] == xy_max:
                return None

        raise ValueError(f'Undesired coverage found! line_number: {line_number}, total_coverage_range: {total_coverage_range}')

    def truncate_range(self, coverage_range, x_min, x_max):
        if coverage_range is None:
            return None

        if coverage_range[0] >= x_min and coverage_range[1] <= x_max:
            return coverage_range

        if coverage_range[1] < x_min or coverage_range[0] > x_max:
            return None

        if coverage_range[1] >= x_min and coverage_range[1] <= x_max:
            return [x_min, coverage_range[1]]

        return [coverage_range[0], x_max]

    def tuning_frequency(self):
        undetected_beacon = self.find_undetected_beacon(0, 4000000)
        return undetected_beacon[0] * 4000000 + undetected_beacon[1]


def main():
    #beacon_zone = BeaconZone('test.txt')
    #line_number = 10
    beacon_zone = BeaconZone('input1.txt')
    line_number = 2000000
    print('# Second question')
    print(f'Tuning frequency of undetected beacon: {beacon_zone.tuning_frequency()}')
    

if __name__ == '__main__':
    main()