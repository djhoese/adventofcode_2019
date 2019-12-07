import sys
from itertools import permutations, chain
import numpy as np
from intcode import run_program


def patient_generator(growing_list):
    idx = 0
    while True:
        if idx >= len(growing_list):
            continue
        val = growing_list[idx]
        if val is None:
            break
        idx += 1
        yield val


def amp(instructions, phase_settings, amp_input=None, feedback_loop=False):
    if amp_input is None:
        amp_input = [0]
        stdin = chain([phase_settings[0]], patient_generator(amp_input))
    else:
        stdin = chain([phase_settings[0]], amp_input)

    stdout_gen = run_program(instructions.copy(), stdin=stdin, stdout=None)
    if len(phase_settings) == 1:
        yield from stdout_gen
    elif feedback_loop and len(phase_settings) == 5:
        for out_val in amp(instructions, phase_settings[1:], amp_input=stdout_gen):
            amp_input.append(out_val)
            yield out_val
    else:
        yield from amp(instructions, phase_settings[1:], amp_input=stdout_gen)


def main():
    instructions = np.loadtxt('input.csv', delimiter=',', dtype=np.int)
    print(max(list(amp(instructions, perm))[-1] for perm in permutations(range(5))))


if __name__ == "__main__":
    sys.exit(main())