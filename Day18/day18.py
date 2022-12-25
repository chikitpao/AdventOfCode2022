""" Advent of Code 2022, Day 18
    Author: Chi-Kit Pao
"""


import os

def debug_output(message):
    # print(message)
    pass

class Droplet:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Quiz:
    def __init__(self, input_file_name: str):
        self.droplet_list = []
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.min_z = None
        self.max_z = None
        self.origin_x = None
        self.origin_y = None
        self.origin_z = None
        self.x_dim = 0
        self.y_dim = 0
        self.z_dim = 0
        self.droplet_cube = []
        self.__read_droplets(input_file_name)

    def __read_droplets(self, input_file_name):
        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))

        for line in lines:
            # Line example: '2,2,2'
            # Relevant information at indices 1, 4, 9 ff.
            tokens = line.split(',')
            x = int(tokens[0])
            y = int(tokens[1])
            z = int(tokens[2])
            self.droplet_list.append(Droplet(x, y, z))
            
            self.min_x = x if self.min_x is None else min(self.min_x, x)
            self.max_x = x if self.max_x is None else max(self.max_x, x)
            self.min_y = y if self.min_y is None else min(self.min_y, y)
            self.max_y = x if self.max_y is None else max(self.max_y, y)
            self.min_z = x if self.min_z is None else min(self.min_z, z)
            self.max_z = x if self.max_z is None else max(self.max_z, z)

        self.origin_x = self.min_x - 1
        self.origin_y = self.min_y - 1
        self.origin_z = self.min_z - 1
        self.x_dim = self.max_x - self.min_x + 3
        self.y_dim = self.max_y - self.min_y + 3
        self.z_dim = self.max_z - self.min_z + 3

        for _ in range(self.x_dim):
            x_array = []
            for _ in range(self.y_dim):
                y_array = [None] * self.z_dim
                x_array.append(y_array)
            self.droplet_cube.append(x_array)

        for droplet in self.droplet_list:
            x, y, z = self.global_to_local(droplet.x, droplet.y, droplet.z)
            self.droplet_cube[x][y][z] = droplet

    def global_to_local(self, x, y, z):
        return x - self.origin_x, y - self.origin_y, z - self.origin_z

    def get_surface_count(self, droplet: Droplet):
        count = 0
        x, y, z = self.global_to_local(droplet.x, droplet.y, droplet.z)
        if self.droplet_cube[x - 1][y][z] is None:
            count += 1
        if self.droplet_cube[x + 1][y][z] is None:
            count += 1
        if self.droplet_cube[x][y - 1][z] is None:
            count += 1
        if self.droplet_cube[x][y + 1][z] is None:
            count += 1
        if self.droplet_cube[x][y][z - 1] is None:
            count += 1
        if self.droplet_cube[x][y][z + 1] is None:
            count += 1
        return count

    def search_outside_surfaces(self):
        count = 0

        def get_neighbors(coordinates):
            neighbors = []
            x = coordinates[0]
            y = coordinates[1]
            z = coordinates[2]
            if x - 1 >= 0:
                neighbors.append((x - 1, y, z))
            if x + 1 < self.x_dim:
                neighbors.append((x + 1, y, z))
            if y - 1 >= 0:
                neighbors.append((x, y - 1, z))
            if y + 1 < self.y_dim:
                neighbors.append((x, y + 1, z))
            if z - 1 >= 0:
                neighbors.append((x, y, z - 1))
            if z + 1 < self.z_dim:
                neighbors.append((x, y, z + 1))
            return neighbors
        
        def index_of_coordinates(coordinates):
            return ((coordinates[0] * self.y_dim) + coordinates[1]) * self.z_dim  + coordinates[2]
        
        visited = [False] * (self.x_dim * self.y_dim * self.z_dim)
        start_coordinates = (0, 0, 0)
        candidates = [start_coordinates]
        visited[index_of_coordinates(start_coordinates)] = True
        while len(candidates) > 0:
            current_cube = candidates.pop(0)
            neighbors = get_neighbors(current_cube)
            for n in neighbors:
                if self.droplet_cube[n[0]][n[1]][n[2]] is not None:
                    count += 1
                    continue
                index = index_of_coordinates(n)
                if visited[index]:
                    continue
                visited[index] = True
                candidates.append(n)
        return count


def main():
    file_names = ['test.txt', 'input1.txt']
    file_names_index = 1

    quiz = Quiz(file_names[file_names_index])
    print('# First question')
    count = 0
    for droplet in quiz.droplet_list:
        count += quiz.get_surface_count(droplet)
    print('Total surface area', count)
    
    print('\n# Second question')
    print('Total outside surface area', quiz.search_outside_surfaces())

if __name__ == '__main__':
    main()