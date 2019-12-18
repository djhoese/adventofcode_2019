import sys
import numpy as np


REPEATING_PATTERN = np.array([0, 1, 0, -1])


def main():
    input_fn = 'input.txt'
    # input_fn = 'example1.txt'
    # input_fn = 'example2.txt'
    with open(input_fn, 'r') as input_file:
        input_values = np.fromiter(list(input_file.read().strip()), dtype=np.int)
        print(input_values.shape)

    in_vals = input_values
    repeating_pattern = np.repeat([REPEATING_PATTERN], in_vals.size // REPEATING_PATTERN.size + 1, axis=0).ravel()[:in_vals.size]
    for phase_idx in range(100):
        out_vals = in_vals.copy()
        for digit_idx in range(in_vals.shape[0]):
            repeat_pat = np.repeat(repeating_pattern, digit_idx + 1)
            repeat_pat = np.roll(repeat_pat, -1)[:in_vals.size]
            out_digit = str((in_vals * repeat_pat).sum())[-1]
            out_vals[digit_idx] = out_digit
        # print(out_vals)
        in_vals = out_vals
    print(out_vals)
    print("".join(str(x) for x in out_vals[:8]))


if __name__ == "__main__":
    sys.exit(main())