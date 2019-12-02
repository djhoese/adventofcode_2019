import numpy as np

INST_SIZE = 4

instructions = np.loadtxt('input.csv', delimiter=',', dtype=np.int)


def run_program(instructions, noun=None, verb=None):
    # Enter error code instructions
    instructions[1] = noun
    instructions[2] = verb

    ip = 0
    while True:
        opcode, param1, param2, dst = instructions[ip:ip + 4]
        if opcode == 1:
            instructions[dst] = instructions[param1] + instructions[param2]
        elif opcode == 2:
            instructions[dst] = instructions[param1] * instructions[param2]
        elif opcode == 99:
            return instructions[0]
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
        ip += 4

if __name__ == "__main__":
    print(run_program(instructions.copy(), noun=12, verb=2))
