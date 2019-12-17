import sys
import numpy as np


REPEATING_PATTERN = np.array([0, 1, 0, -1], dtype=np.int)

from numba import jit

@jit(nopython=True, cache=True)
def calculate_phase(in_vals):
    for phase_idx in range(100):
        out_vals = in_vals.copy()
        for digit_idx in range(in_vals.shape[0] - 2, -1, -1):
            out_vals[digit_idx] = (out_vals[digit_idx] + out_vals[digit_idx + 1]) % 10
        in_vals = out_vals
    return out_vals


def main():
    # input_fn, part2 = 'input.txt', False
    input_fn, part2 = 'input.txt', True
    # input_fn, part2 = 'example1.txt', False
    # input_fn, part2 = 'example2.txt', False
    # input_fn, part2 = 'example3.txt', True
    with open(input_fn, 'r') as input_file:
        input_values = np.fromiter(list(input_file.read().strip()), dtype=np.int)
        print(input_values.shape)

    if part2:
        input_values = np.repeat(input_values[np.newaxis, :], 10000, axis=0).ravel()
        offset = int("".join(str(x) for x in input_values[:7]))
    else:
        offset = 0  # part 1

    in_vals = calculate_phase(input_values)
    print("".join(str(x) for x in in_vals[offset:offset + 8]))


if __name__ == "__main__":
    sys.exit(main())