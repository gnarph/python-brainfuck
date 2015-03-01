#!/usr/bin/python3
"""
Brainfuck interpreter
"""
from collections import defaultdict

# Commands
DP_MOV_RIGHT = '>'
DP_MOV_LEFT = '<'
DP_INCR = '+'
DP_DECR = '-'
DP_OUTPUT = '.'
DP_STORE= ','
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

def main(instructions):
    check_matching_jumps(instructions)
    # Using this as a sparse array instead of a 30,000 element array
    data = defaultdict(int)
    data_pointer = 0
    instruction_pointer = 0

    def mov_right():
        data_pointer += 1

    def mov_left():
        data_pointer -= 1

    def incr():
        data[data_pointer] += 1

    def decr():
        data[data_pointer] -= 1

    def output():
        print data[data_pointer]

    def store():
        pass

    def jumpf():
        pass

    def jumpb():
        pass

    choices = {
        DP_MOV_RIGHT: mov_right,
        DP_MOV_LEFT: mov_left,
        DP_INCR: incr,
        DP_DECR: decr,
        DP_OUTPUT: output,
        DP_STORE: store,
        DP_JUMP_FORWARD: jumpf,
        DP_JUMP_BACKWARD: jumpb,
    }

    end = len(instructions)
    while instruction_pointer < end:
        instruction = instructions[instruction_pointer]
        action = choices[instruction]
        action()

if __name__ == '__main__':
    main()
