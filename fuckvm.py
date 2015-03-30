#!/usr/bin/python3
"""
Brainfuck interpreter
"""
from collections import defaultdict
import sys

from getch import getch

# Commands
INCREMENT_DATA_POINTER = '>'
DECREMENT_DATA_POINTER = '<'
INCREMENT_DATA = '+'
DECREMENT_DATA = '-'
OUTPUT_DATA = '.'
READ_DATA = ','
JUMP_FORWARD = '['
JUMP_BACKWARD = ']'


def check_matching_jumps(instructions):
    """
    All jumps must be 'closed'
    """
    open_jumps = 0
    for instruction in instructions:
        if instruction == JUMP_FORWARD:
            open_jumps += 1
        elif instruction == JUMP_BACKWARD:
            if open_jumps == 0:
                raise Exception('Unmatched back jump')
            open_jumps -= 1
    if open_jumps > 0:
        raise Exception('Unmatched forward jump')
    elif open_jumps < 0:
        raise Exception('Should never happen')


def generate_jump_guide(instructions):
    """
    Where to jump?
    key of dict is origin of jump, value is destination
    """
    openings = []
    jump_guide = {}

    for position, instruction in enumerate(instructions):
        if instruction == JUMP_FORWARD:
            openings.append(position)
        elif instruction == JUMP_BACKWARD:
            forward_position = openings.pop()
            backward_position = position
            jump_guide[forward_position] = backward_position
            jump_guide[backward_position] = forward_position
    return jump_guide


class FuckVM(object):
    """
    brainfuck virtual machine
    """

    def __init__(self, instructions):
        """
        Initialize with a program
        """
        self.instructions = instructions
        check_matching_jumps(instructions)
        # Using this as a sparse array instead of a 30,000 element array
        self.data = defaultdict(int)
        self.data_pointer = 0
        self.instruction_pointer = 0
        self._dispatch = {
            INCREMENT_DATA_POINTER: self.increment_data_pointer,
            DECREMENT_DATA_POINTER: self.decrement_data_pointer,
            INCREMENT_DATA: self.increment_data,
            DECREMENT_DATA: self.decrement_data,
            OUTPUT_DATA: self.output,
            READ_DATA: self.store,
            JUMP_FORWARD: self.jump_forward,
            JUMP_BACKWARD: self.jump_backward,
        }
        self.jump_guide = generate_jump_guide(instructions)

    @staticmethod
    def _do_nothing():
        """
        Do nothing on an invalid instruction
        """
        pass

    def dispatch(self, cmd):
        """
        Get method
        """
        return self._dispatch.get(cmd, self._do_nothing)

    def data_at_ptr(self):
        """
        Get data at datapointer
        """
        return self.data[self.data_pointer]

    def increment_data_pointer(self):
        """
        increment data pointer
        """
        self.data_pointer += 1

    def decrement_data_pointer(self):
        """
        decrement data pointer
        """
        self.data_pointer -= 1

    def increment_data(self):
        """
        Increment data at pointer
        """
        self.data[self.data_pointer] += 1

    def decrement_data(self):
        """
        Decrement data at pointer
        """
        self.data[self.data_pointer] -= 1

    def output(self):
        """
        Print data at pointer
        """
        datum = self.data_at_ptr()
        try:
            char = chr(datum)
        except ValueError:
            char = datum
        sys.stdout.write('%s' % char)
        sys.stdout.flush()

    def store(self):
        """
        Read single char
        """
        character = getch()
        self.data[self.data_pointer] = ord(character)

    def _get_jump_destination(self):
        """
        Find destination of jump
        """
        return self.jump_guide[self.instruction_pointer]

    def jump_forward(self):
        """
        Jump forward
        """
        if not self.data_at_ptr():
            self.instruction_pointer = self._get_jump_destination()

    def jump_backward(self):
        """
        Jump backward
        """
        if self.data_at_ptr():
            self.instruction_pointer = self._get_jump_destination()

    def fetch(self):
        """
        Fetch next instruction
        """
        return self.instructions[self.instruction_pointer]

    def execute(self):
        """
        Run instructions
        """
        end = len(self.instructions)
        while self.instruction_pointer < end:
            instruction = self.fetch()
            action = self.dispatch(instruction)
            action()
            self.instruction_pointer += 1

if __name__ == '__main__':
    brainfuck_vm = FuckVM(sys.argv[1])
    brainfuck_vm.execute()
