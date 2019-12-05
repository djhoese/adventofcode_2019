import numpy as np


def get_args(instructions, ip, param_modes, num_args):
    for i in range(num_args):
        yield instructions[ip + i + 1] if param_modes[i] else instructions[instructions[ip + i + 1]]


def run_program(instructions, noun=None, verb=None):
    # Enter error code instructions
    if noun is not None:
        instructions[1] = noun
    if verb is not None:
        instructions[2] = verb

    ip = 0
    while True:
        opcode = instructions[ip]
        opcode = f"{opcode:05d}"
        param_modes = [int(x) for x in reversed(opcode[:-2])]
        opcode = int(opcode[-2:])

        if opcode == 1:
            arg1, arg2 = get_args(instructions, ip, param_modes, 2)
            dst = instructions[ip + 3]
            instructions[dst] = arg1 + arg2
            ip += 4
        elif opcode == 2:
            arg1, arg2 = get_args(instructions, ip, param_modes, 2)
            dst = instructions[ip + 3]
            instructions[dst] = arg1 * arg2
            ip += 4
        elif opcode == 3:
            user_input = int(input("Enter single digit:"))
            dst = instructions[ip + 1]
            instructions[dst] = user_input
            ip += 2
        elif opcode == 4:
            arg1, = get_args(instructions, ip, param_modes, 1)
            print(arg1)
            ip += 2
        elif opcode == 99:
            return instructions[0]
        else:
            raise ValueError(f"Unknown opcode: {opcode}")


if __name__ == "__main__":
    instructions = np.loadtxt('input.csv', delimiter=',', dtype=np.int)
    run_program(instructions.copy())
