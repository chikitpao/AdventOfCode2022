""" Advent of Code 2022, Day 13, Part2
    Author: Chi-Kit Pao
"""

import os


def debug_output(message):
    print(message)
    #pass


class Signal:
    TYPE_LIST_BEGIN = 0
    TYPE_LIST_END = 1
    TYPE_INT = 2
    TYPE_DATA_END = 3

    PSEUDO_LIST_MODE_NONE = 0
    PSEUDO_LIST_MODE_BEGIN = 1
    PSEUDO_LIST_MODE_INT = 2
    PSEUDO_LIST_MODE_END = 3

    def __init__(self, data_string):
        # data strings act like instructions of a programm
        self.data_string = data_string
        self.greater_count = 0  # greater than a number of other elements

        # Remark: Update method "reset_process_data" after adding / changing initialization 
        self.data_pointer = 0
        self.pseudo_list_mode = Signal.PSEUDO_LIST_MODE_NONE
        self.list_to_int_level = 0

    def get_element_type(self):
        if self.data_pointer >= len(self.data_string):
            return Signal.TYPE_DATA_END
        elif self.pseudo_list_mode == Signal.PSEUDO_LIST_MODE_END: 
            return Signal.TYPE_LIST_END
        elif self.data_string[self.data_pointer] == '[':
            return Signal.TYPE_LIST_BEGIN
        elif self.data_string[self.data_pointer] == ']':
            return Signal.TYPE_LIST_END
        elif self.data_string[self.data_pointer].isnumeric():
            return Signal.TYPE_INT
        else:
            assert False, f'Unknown element: {self.data_string[self.data_pointer]}'

    def get_int_string(self, current_data_pointer):
        start_data_pointer = current_data_pointer
        end_data_pointer = current_data_pointer
        while self.data_string[end_data_pointer].isnumeric():
            end_data_pointer += 1
        return self.data_string[start_data_pointer : end_data_pointer]

    def process_int_as_list(self):
        # REMARK: Keep track over list-to-int conversion level for proper 
        # number of end square brackets
        self.pseudo_list_mode = Signal.PSEUDO_LIST_MODE_BEGIN
        self.list_to_int_level += 1

    def process_element(self):
        if self.pseudo_list_mode == Signal.PSEUDO_LIST_MODE_BEGIN:
            self.pseudo_list_mode = Signal.PSEUDO_LIST_MODE_INT
            return '['
        elif self.pseudo_list_mode == Signal.PSEUDO_LIST_MODE_INT:
            current_data_pointer = self.data_pointer
            self.update_data_pointer()
            self.pseudo_list_mode = Signal.PSEUDO_LIST_MODE_END
            return self.get_int_string(current_data_pointer)
        elif self.pseudo_list_mode == Signal.PSEUDO_LIST_MODE_END:
            self.list_to_int_level -= 1
            if self.list_to_int_level == 0:
                self.update_data_pointer()
                self.pseudo_list_mode = Signal.PSEUDO_LIST_MODE_NONE
            return ']'
        elif self.data_string[self.data_pointer] == '[':
            self.update_data_pointer()
            return '['
        elif self.data_string[self.data_pointer] == ']':
            self.update_data_pointer()
            return ']'
        elif self.data_string[self.data_pointer].isnumeric():
            current_data_pointer = self.data_pointer
            self.update_data_pointer()
            return self.get_int_string(current_data_pointer)
        else:
            assert False, f'Unknown element: {self.data_string[self.data_pointer]}'

    def reset_process_data(self):
        self.data_pointer = 0
        self.pseudo_list_mode = Signal.PSEUDO_LIST_MODE_NONE
        self.list_to_int_level = 0

    def update_data_pointer(self):
        assert self.data_pointer < len(self.data_string)

        if self.pseudo_list_mode == Signal.PSEUDO_LIST_MODE_END and self.list_to_int_level == 0:
            if self.data_string[self.data_pointer] == ',':
                self.data_pointer += 1
        elif self.data_string[self.data_pointer] == '[':
            self.data_pointer += 1
        elif self.data_string[self.data_pointer] == ']':
           self.data_pointer += 1
           if self.data_pointer < len(self.data_string) and self.data_string[self.data_pointer] == ',':
                self.data_pointer += 1
        elif self.data_string[self.data_pointer].isnumeric():
            while self.data_string[self.data_pointer].isnumeric():
                self.data_pointer += 1
            if self.pseudo_list_mode != Signal.PSEUDO_LIST_MODE_INT:
                if self.data_string[self.data_pointer] == ',':
                    self.data_pointer += 1


class SignalStorage2:
    def __init__(self, input_file_name: str):
        self.signals = []
        self.divider1 = Signal('[[2]]')
        self.divider2 = Signal('[[6]]')
        self.signals.append(self.divider1)
        self.signals.append(self.divider2)
        self.less_than_count = None   # number of elements which are "less than" oneself 

        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            i = 0
            while i < len(lines):
                self.signals.append(Signal(lines[i + 0]))
                self.signals.append(Signal(lines[i + 1]))
                i += 3
        
        self.less_than_count = [0] * len(self.signals)
        
        for i in range(len(self.signals)):
            for j in range(len(self.signals)):
                if i >= j:
                    continue

                result = self.check_signals(self.signals[i], self.signals[j])
                self.signals[i].reset_process_data()
                self.signals[j].reset_process_data()
                if result:
                    self.less_than_count[i] += 1
                    self.signals[j].greater_count += 1
                else:
                    self.less_than_count[j] += 1
                    self.signals[i].greater_count += 1

        self.test_transitivity()

        # Sort signals in ascending order.
        self.signals.sort(key = (lambda x: x.greater_count))

    # REMARK: Relation appears to be transitive.
    def check_signals(self, left_signal, right_signal):        
        left_element_type = left_signal.get_element_type()
        right_element_type = right_signal.get_element_type()
        while left_element_type != Signal.TYPE_DATA_END:
            left_element_type = left_signal.get_element_type()
            right_element_type = right_signal.get_element_type()

            if left_element_type == right_element_type:
                if left_element_type == Signal.TYPE_LIST_BEGIN or left_element_type == Signal.TYPE_LIST_END:
                    left_signal.process_element()
                    right_signal.process_element()
                elif left_element_type == Signal.TYPE_INT:
                    left_int = int(left_signal.process_element())
                    right_int = int(right_signal.process_element())
                    if left_int < right_int:
                        return True
                    elif left_int > right_int:
                        return False
            else:
                if left_element_type == Signal.TYPE_LIST_BEGIN:
                    if right_element_type == Signal.TYPE_LIST_END:
                        return False
                    else:
                        assert right_element_type == Signal.TYPE_INT
                        left_signal.process_element()
                        right_signal.process_int_as_list()
                        right_signal.process_element()
                elif left_element_type == Signal.TYPE_LIST_END:
                    if right_element_type == Signal.TYPE_LIST_BEGIN:
                        return True
                    else:
                        assert right_element_type == Signal.TYPE_INT
                        return True
                else:
                    assert left_element_type == Signal.TYPE_INT
                    if right_element_type == Signal.TYPE_LIST_BEGIN:
                        left_signal.process_int_as_list()
                        left_signal.process_element()
                        right_signal.process_element()
                    else:
                        assert right_element_type == Signal.TYPE_LIST_END
                        return False

            left_element_type = left_signal.get_element_type()
            right_element_type = right_signal.get_element_type()
            if left_element_type != Signal.TYPE_DATA_END and right_element_type == Signal.TYPE_DATA_END:
                return False        

        if right_element_type != Signal.TYPE_DATA_END:
            return True
        else:
            assert False, "both signals ran out of items"

    def get_decorder_key(self):
        divider1_index = self.signals.index(self.divider1) + 1
        divider2_index = self.signals.index(self.divider2) + 1
        return divider1_index * divider2_index

    def test_transitivity(self):
        print('# Test transitivity')
        print(len(self.signals), self.less_than_count)
        for i in range(302):
            if i not in self.less_than_count:
                print(f'{i} not in self.less_than_count')


def main():
    signal_storage = SignalStorage2('input1.txt')
    print('# Second question')
    print(f'Decorder key for the distress signal: {signal_storage.get_decorder_key()}')


if __name__ == '__main__':
    main()