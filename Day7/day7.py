""" Advent of Code 2022, Day 7
    Author: Chi-Kit Pao
"""

import os


small_folders_total_size = 0
minimum_size_to_be_deleted = 0
deletion_candidate = None


class TestItem:
    def __init__(self, parent, name, type, size):
        self.parent = parent
        self.name = name
        self.type = type  # 'd' or 'f'
        self.size = size
        self.content = {}  # name -> TestItem

    def calculate_folder_size(self):
        assert (self.type == 'd')
        
        total_size = 0
        for item in self.content.values():
            if item.type == 'f':
                total_size += item.size
            else:
                total_size += item.calculate_folder_size()

        # print(f"folder {self.name}: total size {total_size}")

        if total_size < 100000:
            global small_folders_total_size
            small_folders_total_size += total_size

        return total_size

    def find_folder_to_be_deleted(self, minimum_size):
        total_size = self.calculate_folder_size()
        size_difference = total_size - minimum_size
        if total_size >= minimum_size:
            global deletion_candidate
            if deletion_candidate is None:
                deletion_candidate = (self, size_difference, total_size)
            else:
                candidate_item, candidate_size_difference, candidate_total_size = deletion_candidate
                if size_difference < candidate_size_difference:
                    deletion_candidate = (self, size_difference, total_size)

        for item in self.content.values():
            if item.type == 'd':
                 item.find_folder_to_be_deleted(minimum_size)

class TestFileSystem:
    def __init__(self, input_file_name: str):
        self.root_dir = TestItem(None, '/', 'd', 0)
        self.current_dir = self.root_dir 
        self.list_mode_dir = None

        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            rows = list(map(lambda s: s.replace('\n', ''), f.readlines()))

            for row in rows:
                self.process_row(row)

    def process_row(self, row):
        if row.startswith('$ cd '):
            # '/', '..' or directory name
            arg = row[len('$ cd '):]
            if arg == '/':
                self.list_mode_dir = None
                self.current_dir = self.root_dir
            elif arg == '..':
                self.list_mode_dir = None
                assert (self.current_dir.parent is not None)
                self.current_dir = self.current_dir.parent
            else:
                self.list_mode_dir = None
                self.current_dir = self.current_dir.content[arg]
        elif row == '$ ls':
            self.list_mode_dir = self.current_dir
        elif row.startswith('dir '):
            assert (self.list_mode_dir is not None)
            dir_name = row [len('dir '):]
            self.current_dir.content[dir_name] = TestItem(self.current_dir, dir_name, 'd', 0)
            pass
        elif len(row) > 0 and row[0].isnumeric():
            assert (self.list_mode_dir is not None)
            args = row.split()
            size = int(args[0])
            file_name = args[1]
            self.current_dir.content[file_name] = TestItem(self.current_dir, file_name, 'f', size)
            pass
        elif len(row) == 0:
            self.list_mode_dir = None
        else:
            raise ValueError(f"Cannot parse row: {row}")


def main():
    tfs = TestFileSystem('input1.txt')
    root_folder_size = tfs.root_dir.calculate_folder_size()
    
    print('# First question')
    print(f'Total sizes of small directories: {small_folders_total_size}')

    print('# Second question')
    # The total disk space available to the filesystem is 70000000. To run the update, you need 
    # unused space of at least 30000000. You need to find a directory you can delete that will 
    # free up enough space to run the update.
    print(f'root folder size: {root_folder_size}')
    total_space = 70_000_000
    required_space = 30_000_000
    global minimum_size_to_be_deleted
    minimum_size_to_be_deleted = root_folder_size - (total_space - required_space)
    print(f'minimum size to be deleted: {minimum_size_to_be_deleted}')
    tfs.root_dir.find_folder_to_be_deleted(minimum_size_to_be_deleted)
    if deletion_candidate is None:
        print('Cannot find folder to delete!')
    else:
        candidate_item, candidate_size_difference, candidate_total_size = deletion_candidate
        print(f'Will delete folder {candidate_item.name}, size: {candidate_total_size}.')


if __name__ == '__main__':
    main()