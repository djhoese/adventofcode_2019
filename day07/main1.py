import sys
from itertools import permutations, chain
import numpy as np
from intcode import run_program


def fake_stdin(permutation):
    for phase_setting in permutation:
        yield phase_setting


def amp(instructions, phase_settings, input=[0]):
    stdin = chain([phase_settings[0]], input)
    stdout = []
    run_program(instructions.copy(), stdin=stdin, stdout=stdout)
    if len(phase_settings) == 1:
        return stdout[-1]
    return amp(instructions, phase_settings[1:], input=stdout)


def main():
    instructions = np.loadtxt('input.csv', delimiter=',', dtype=np.int)
    print(max(amp(instructions, perm) for perm in permutations(range(5))))


if __name__ == "__main__":
    sys.exit(main())