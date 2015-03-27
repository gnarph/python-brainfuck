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
    Brainfuck virtual machine
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

    def data_at_ptr(self):
        return self.data[self.data_pointer]

    def mov_right(self):
        """
        increment data pointer
        """
        self.data_pointer += 1

    def mov_left(self):
        """
        decrement data pointer
        """
        self.data_pointer -= 1

    def incr(self):
        """
        Increment data at pointer
        """
        self.data[self.data_pointer] += 1

    def decr(self):
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

    def jumpf(self):
        """
        Jump forward
        """
        if self.data_at_ptr() != 0:
            return
        ptr = self.instruction_pointer + 1
        opn = 1
        while ptr < len(self.instructions):
            inst = self.instructions[ptr]
            if inst == IP_JUMP_FORWARD:
                opn += 1
            elif inst == IP_JUMP_BACKWARD:
                opn -= 1
            if opn == 0:
                break
            ptr += 1
        self.instruction_pointer = ptr

    def jumpb(self):
        """
        Jump backward
        """
        if not self.data_at_ptr():
            return
        ptr = self.instruction_pointer - 1
        opn = -1
        while 0 < ptr < len(self.instructions):
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
        instruction = self.instructions[self.instruction_pointer]
        return instruction

    def execute(self):
        """
        Run instructions
        """
        choices = {
            DP_MOV_RIGHT: self.mov_right,
            DP_MOV_LEFT: self.mov_left,
            DP_INCR: self.incr,
            DP_DECR: self.decr,
            DP_OUTPUT: self.output,
            DP_STORE: self.store,
            IP_JUMP_FORWARD: self.jumpf,
            IP_JUMP_BACKWARD: self.jumpb,
        }

        end = len(self.instructions)
        while self.instruction_pointer < end:
            instruction = self.fetch()
            try:
                action = choices[instruction]
            except KeyError:
                continue
            else:
                action()
            finally:
                self.instruction_pointer += 1

if __name__ == '__main__':
    brainfuck_vm = FuckVM(sys.argv[1])
    brainfuck_vm.execute()
