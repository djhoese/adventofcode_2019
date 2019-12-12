import sys
import numpy as np
from itertools import combinations


def get_total_energy(positions, velocities):
    pot = np.sum(np.abs(positions), axis=1)
    kin = np.sum(np.abs(velocities), axis=1)
    return np.sum(pot * kin)


def main():
    fn = 'input.txt'
    num_steps = 1000
    # fn = 'example1.txt'
    # num_steps = 10
    # fn = 'example2.txt'
    # num_steps = 100
    with open(fn) as in_file:
        positions = []
        for line in in_file:
            line = line.strip()[1:-1].replace('x=', '').replace(' y=', '').replace(' z=', '')
            positions.append([int(x) for x in line.split(',')])
    positions = np.array(positions)
    velocities = np.zeros_like(positions)

    for step_num in range(num_steps):
        # compute gravity adjustments
        for moon1_idx, moon2_idx in combinations(range(positions.shape[0]), 2):
            adjust_lt = positions[moon1_idx] < positions[moon2_idx]
            adjust_eq = positions[moon1_idx] == positions[moon2_idx]
            adjust = np.where(adjust_lt, 1, -1)
            adjust[adjust_eq] = 0
            velocities[moon1_idx] += adjust
            velocities[moon2_idx] -= adjust

        # update positions
        positions += velocities
    print(get_total_energy(positions, velocities))


if __name__ == "__main__":
    sys.exit(main())