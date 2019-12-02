import numpy as np
from main1 import run_program

DESIRED = 19690720
INSTRUCTIONS = np.loadtxt('input.csv', delimiter=',', dtype=np.int)
MEMORY = np.zeros_like(INSTRUCTIONS)


def find_noun_verb(desired):
    for noun in range(100):
        for verb in range(100):
            MEMORY[:] = INSTRUCTIONS
            result = run_program(MEMORY, noun=noun, verb=verb)
            if result == desired:
                return noun, verb

if __name__ == "__main__":
    noun, verb = find_noun_verb(DESIRED)
    print(100 * noun + verb)