import sys
import numpy as np
from main1 import amp
from itertools import permutations


def main():
    instructions = np.loadtxt('input.csv', delimiter=',', dtype=np.int)
    print(max(list(amp(instructions, perm, feedback_loop=True))[-1] for perm in permutations(range(5, 10))))


if __name__ == "__main__":
    sys.exit(main())
