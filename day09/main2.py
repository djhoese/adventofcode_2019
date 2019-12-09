import sys
import numpy as np
from intcode import IntCodeComputer, parse_args


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    comp = IntCodeComputer(stdin=iter([2]))
    print(list(comp.run(instructions)))


if __name__ == "__main__":
    sys.exit(main())
