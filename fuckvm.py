#!/usr/bin/python3
"""
Brainfuck interpreter
"""
from collections import defaultdict
import sys

from getch import getch

# Commands
DP_MOV_RIGHT = '>'
DP_MOV_LEFT = '<'
DP_INCR = '+'
DP_DECR = '-'
DP_OUTPUT = '.'
DP_STORE = ','
IP_JUMP_FORWARD = '['
IP_JUMP_BACKWARD = ']'


def check_matching_jumps(instructions):
    """
    All jumps must be 'closed'
    """
    open_jumps = 0
    for instruction in instructions:
        if instruction == IP_JUMP_FORWARD:
            open_jumps += 1
        elif instruction == IP_JUMP_BACKWARD:
            if open_jumps == 0:
                raise Exception('Unmatched back jump')
            open_jumps -= 1
    if open_jumps > 0:
        raise Exception('Unmatched forward jump')
    elif open_jumps < 0:
        raise Exception('Should never happen')


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
            DP_MOV_RIGHT: self.increment_data_pointer,
            DP_MOV_LEFT: self.decrement_data_pointer,
            DP_INCR: self.increment_data,
            DP_DECR: self.decrement_data,
            DP_OUTPUT: self.output,
            DP_STORE: self.store,
            IP_JUMP_FORWARD: self.jump_forward,
            IP_JUMP_BACKWARD: self.jump_backward,
        }

    def dispatch(self, cmd):
        """
        Get method
        """
        return self._dispatch[cmd]

    def data_at_ptr(self):
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
        try:
            char = chr(self.data[self.data_pointer])
        except ValueError:
            char = self.data[self.data_pointer]
        sys.stdout.write('%s' % char)
        sys.stdout.flush()

    def store(self):
        """
        Read single char
        """
        c = getch()
        self.data[self.data_pointer] = c

    def jump_forward(self):
        """
        Jump forward
        """
        if self.data_at_ptr() != 0:
            return
        ptr = self.instruction_pointer + 1
        opn = 1
        li = len(self.instructions)
        while 0 < ptr < li:
            inst = self.instructions[ptr]
            if inst == IP_JUMP_FORWARD:
                opn += 1
            elif inst == IP_JUMP_BACKWARD:
                opn -= 1
            if opn == 0:
                break
            ptr += 1
        self.instruction_pointer = ptr

    def jump_backward(self):
        """
        Jump backward
        """
        if not self.data_at_ptr():
            return
        ptr = self.instruction_pointer - 1
        opn = -1
        li = len(self.instructions)
        while 0 < ptr < li:
            inst = self.instructions[ptr]
            if inst == IP_JUMP_FORWARD:
                opn += 1
            elif inst == IP_JUMP_BACKWARD:
                opn -= 1
            if opn == 0:
                break
            ptr -= 1
        self.instruction_pointer = ptr

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
            try:
                action = self.dispatch(instruction)
            except KeyError:
                continue
            else:
                action()
            finally:
                self.instruction_pointer += 1

if __name__ == '__main__':
    brainfuck_vm = FuckVM(sys.argv[1])
    brainfuck_vm.execute()
