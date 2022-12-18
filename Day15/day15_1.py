""" Advent of Code 2022, Day 15, Part 1
    Author: Chi-Kit Pao
"""


import os


def debug_output(message):
    #print(message)
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

    def beacon_free_fields_at_line(self, line_number):
        # total_coverage_range: List of non-overlapping coverage ranges, None if empty
        total_coverage_range = None
        for sensor in self.sensors:
            coverage_range = sensor.coverage_at_line(line_number)
            if coverage_range is not None:
                if total_coverage_range is None:
                    total_coverage_range = []
                    total_coverage_range.append(coverage_range)
                    self.debug_total_coverage_range(coverage_range, total_coverage_range)
                    continue
                
                # Process from the end of list, extend total_coverage_range[] if necessary
                i = len(total_coverage_range) - 1
                while i >= 0:
                    if i == len(total_coverage_range) - 1:
                        if coverage_range[0] > total_coverage_range[i][1] + 1:
                            # New coverage range is behind the last existing coverage range and 
                            # cannot be merged to this range -> Append new range
                            total_coverage_range.append(coverage_range)
                            self.debug_total_coverage_range(coverage_range, total_coverage_range)
                        elif coverage_range[1] > total_coverage_range[i][1]:
                            # New coverage range is behind the last existing coverage range and 
                            # can be merged to this range -> Extend end of total_coverage_range[i][1]
                            total_coverage_range[i][1] = coverage_range[1]
                            self.debug_total_coverage_range(coverage_range, total_coverage_range)
                    else:
                        if coverage_range[0] > total_coverage_range[i][1] + 1 and coverage_range[1] < total_coverage_range[i + 1][0] - 1:
                            # New coverage range is between current and next existing coverage ranges and 
                            # cannot be merged -> Insert new range
                            total_coverage_range.insert(i + 1, coverage_range)
                            self.debug_total_coverage_range(coverage_range, total_coverage_range)
                        else:
                            if coverage_range[1] >= total_coverage_range[i + 1][0] - 1:
                                if coverage_range[0] > total_coverage_range[i][1] + 1:
                                    if coverage_range[0] < total_coverage_range[i + 1][0]:
                                        # Merge next range with new range
                                        total_coverage_range[i + 1][0] = coverage_range[0]
                                        self.debug_total_coverage_range(coverage_range, total_coverage_range)
                                else:
                                    # Merge next range with current range
                                    total_coverage_range[i][1] = total_coverage_range[i + 1][1]
                                    total_coverage_range.pop(i + 1)
                                    self.debug_total_coverage_range(coverage_range, total_coverage_range)
                            elif coverage_range[1] >= total_coverage_range[i][1] + 1 and coverage_range[0] <= total_coverage_range[i][1]:
                                # Merge current range with new range
                                total_coverage_range[i][1] = coverage_range[1]
                                self.debug_total_coverage_range(coverage_range, total_coverage_range)

                    if i == 0:
                        if coverage_range[1] < total_coverage_range[i][0] - 1:
                            # New coverage range is in front of the first existing coverage range and 
                            # cannot be merged to this range -> Insert new range to the front
                            total_coverage_range.insert(0, coverage_range)
                            self.debug_total_coverage_range(coverage_range, total_coverage_range)
                        elif coverage_range[1] >= total_coverage_range[i][0]:
                            if coverage_range[0] < total_coverage_range[i][0]:
                                # New coverage range is in front the first existing coverage range and 
                                # can be merged to this range -> Extend start of total_coverage_range[i][1]
                                total_coverage_range[i][0] = coverage_range[0]
                                self.debug_total_coverage_range(coverage_range, total_coverage_range)
                    i -= 1

        if total_coverage_range is None:
            return 
        
        debug_output(f'total_coverage_range {total_coverage_range}')
        for sensor in self.sensors:
            debug_output(f'sensor {sensor.coverage_at_line(line_number)}')

        total_coverage_count = 0
        for coverage_range in total_coverage_range:
            total_coverage_count += coverage_range[1] - coverage_range[0] + 1
        for beacon in self.beacons:
            for coverage_range in total_coverage_range:
               if beacon[1] == line_number and beacon[0] >= coverage_range[0] and beacon[0] <= coverage_range[1]:
                    debug_output(f'y {line_number} -> beacon found: x {beacon[0]} in ({coverage_range[0]},{coverage_range[1]})')
                    total_coverage_count -= 1
                    if total_coverage_count <= 0:
                        return 0
        for sensor in self.sensors:
            for coverage_range in total_coverage_range:
               if sensor.y_sensor == line_number and sensor.x_sensor >= coverage_range[0] and sensor.x_sensor <= coverage_range[1]:
                    debug_output(f'y {line_number} -> signal found: x {sensor.x_sensor} in ({coverage_range[0]},{coverage_range[1]})')
                    total_coverage_count -= 1
                    if total_coverage_count <= 0:
                        return 0

        return total_coverage_count
    
    def debug_total_coverage_range(self, coverage_range, total_coverage_range):
         debug_output(f'coverage_range: {coverage_range}, total_coverage_range: {total_coverage_range}')


def main():
    #beacon_zone = BeaconZone('test.txt')
    #line_number = 10
    beacon_zone = BeaconZone('input1.txt')
    line_number = 2000000
    print('# First question')
    print(f'Beacon free field: {beacon_zone.beacon_free_fields_at_line(line_number)}')
    

if __name__ == '__main__':
    main()