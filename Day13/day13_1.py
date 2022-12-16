""" Advent of Code 2022, Day 13
    Author: Chi-Kit Pao
"""

import os


def debug_output(message):
    #print(message)
    pass


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
        self.data_pointer = 0
        self.pseudo_list_mode = Signal.PSEUDO_LIST_MODE_NONE
        self.list_to_int_level = 0
        pass

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


class SignalStorage:
    def __init__(self, input_file_name: str):
        self.left_signals = []
        self.right_signals = []
        self.result = []  # pair with return value True, one-based

        file_path = os.path.dirname(__file__)
        with open(os.path.join(file_path, input_file_name), 'r') as f:
            lines = list(map(lambda s: s.replace('\n', '').strip(), f.readlines()))
            i = 0
            while i < len(lines):
                # line 0: Monkey 0:
                self.left_signals.append(Signal(lines[i + 0]))
                self.right_signals.append(Signal(lines[i + 1]))
                i += 3

        assert len(self.left_signals) == len(self.right_signals)

        for i in range(len(self.left_signals)):
            debug_output(f'{i + 1} left {self.left_signals[i].data_string}')
            debug_output(f'{i + 1} right {self.right_signals[i].data_string}')

            result = self.check_signals(self.left_signals[i], self.right_signals[i])
            debug_output(f'{i + 1} result {result}')
            debug_output('')
            if result:
                self.result.append(i + 1)

    def check_signals(self, left_signal, right_signal):        
        left_element_type = left_signal.get_element_type()
        right_element_type = right_signal.get_element_type()
        while left_element_type != Signal.TYPE_DATA_END:
            left_element_type = left_signal.get_element_type()
            right_element_type = right_signal.get_element_type()

            if left_element_type == right_element_type:
                if left_element_type == Signal.TYPE_LIST_BEGIN or left_element_type == Signal.TYPE_LIST_END:
                    debug_output(f'left: {left_signal.process_element()}')
                    debug_output(f'right: {right_signal.process_element()}')
                    pass
                elif left_element_type == Signal.TYPE_INT:
                    left_int = int(left_signal.process_element())
                    right_int = int(right_signal.process_element())
                    debug_output(f'left: {left_int}')
                    debug_output(f'right: {right_int}')
                    if left_int < right_int:
                        return True
                    elif left_int > right_int:
                        return False
            else:
                if left_element_type == Signal.TYPE_LIST_BEGIN:
                    if right_element_type == Signal.TYPE_LIST_END:
                        # Only process for output
                        debug_output(f'left: {left_signal.process_element()}')
                        debug_output(f'right: {right_signal.process_element()}')
                        return False
                    else:
                        assert right_element_type == Signal.TYPE_INT
                        debug_output(f'left: {left_signal.process_element()}')
                        right_signal.process_int_as_list()
                        debug_output(f'right(int as list): {right_signal.process_element()}')
                elif left_element_type == Signal.TYPE_LIST_END:
                    if right_element_type == Signal.TYPE_LIST_BEGIN:
                         # Only process for output
                        debug_output(f'left: {left_signal.process_element()}')
                        debug_output(f'right: {right_signal.process_element()}')
                        return True
                    else:
                        assert right_element_type == Signal.TYPE_INT
                         # Only process for output
                        debug_output(f'left: {left_signal.process_element()}')
                        debug_output(f'right: {right_signal.process_element()}')
                        return True
                else:
                    assert left_element_type == Signal.TYPE_INT
                    if right_element_type == Signal.TYPE_LIST_BEGIN:
                        left_signal.process_int_as_list()
                        debug_output(f'left(int as list): {left_signal.process_element()}')
                        debug_output(f'right: {right_signal.process_element()}')
                    else:
                        assert right_element_type == Signal.TYPE_LIST_END
                        # Only process for output
                        debug_output(f'left: {left_signal.process_element()}')
                        debug_output(f'right: {right_signal.process_element()}')
                        return False

            left_element_type = left_signal.get_element_type()
            right_element_type = right_signal.get_element_type()
            if left_element_type != Signal.TYPE_DATA_END and right_element_type == Signal.TYPE_DATA_END:
                 # Only process for output
                debug_output(f'left: {left_signal.process_element()}')
                debug_output(f'right: data end')
                return False        

        if right_element_type != Signal.TYPE_DATA_END:
            return True
        else:
            assert False, "both signals ran out of items"


def main():
    
    print('# First question')
    signal_storage = SignalStorage('input1.txt')
    print(f'Sum of indices: {sum(signal_storage.result)}')


if __name__ == '__main__':
    main()