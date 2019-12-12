import sys
import numpy as np
from itertools import combinations
from numba import jit
from math import gcd
from functools import reduce


def get_total_energy(positions, velocities):
    pot = np.sum(np.abs(positions), axis=1)
    kin = np.sum(np.abs(velocities), axis=1)
    return np.sum(pot * kin)


@jit(nopython=True, cache=True)
def perform_step(positions, velocities, moon_combos):
    for moon1_idx, moon2_idx in moon_combos:
        adjust_lt = positions[moon1_idx] < positions[moon2_idx]
        adjust_eq = positions[moon1_idx] == positions[moon2_idx]
        adjust = np.where(adjust_lt, 1, -1)
        adjust[adjust_eq] = 0
        velocities[moon1_idx] += adjust
        velocities[moon2_idx] -= adjust
    return positions, velocities


@jit(nopython=True, cache=True)
def run_loop(positions, velocities):
    num_steps = 0
    # start_state = np.array([positions, velocities])
    # moon_combos = list(combinations(range(positions.shape[0]), 2))
    moon_combos = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    start_pos = positions.copy()
    start_vel = velocities.copy()
    while True:
        # compute gravity adjustments
        for moon1_idx, moon2_idx in moon_combos:
            adjust_lt = positions[moon1_idx] < positions[moon2_idx]
            adjust_eq = positions[moon1_idx] == positions[moon2_idx]
            adjust = np.where(adjust_lt, 1, -1)
            adjust[adjust_eq] = 0
            velocities[moon1_idx] += adjust
            velocities[moon2_idx] -= adjust

        # update positions
        positions += velocities

        # compute historical positions and velocities
        num_steps += 1
        # if (start_state[0, :] == positions).all() and (start_state[1, :] == velocities).all():
        if (start_pos == positions).all() and (start_vel == velocities).all():
            return num_steps



@jit(nopython=True, cache=True)
def run_loop_per_axis(positions, velocities):
    num_steps = 0
    # moon_combos = list(combinations(range(positions.shape[0]), 2))
    moon_combos = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    start_pos = positions.copy()
    start_vel = velocities.copy()
    while True:
        # compute gravity adjustments
        for moon1_idx, moon2_idx in moon_combos:
            if positions[moon1_idx] < positions[moon2_idx]:
                velocities[moon1_idx] += 1
                velocities[moon2_idx] -= 1
            elif positions[moon1_idx] > positions[moon2_idx]:
                velocities[moon1_idx] -= 1
                velocities[moon2_idx] += 1

        # update positions
        positions += velocities

        # compute historical positions and velocities
        num_steps += 1
        # if (start_state[0, :] == positions).all() and (start_state[1, :] == velocities).all():
        if (start_pos == positions).all() and (start_vel == velocities).all():
            return num_steps


def main():
    fn = 'input.txt'
    # fn = 'example1.txt'
    # fn = 'example2.txt'
    with open(fn) as in_file:
        positions = []
        for line in in_file:
            line = line.strip()[1:-1].replace('x=', '').replace(' y=', '').replace(' z=', '')
            positions.append([int(x) for x in line.split(',')])
    positions = np.array(positions).astype(np.int)
    velocities = np.zeros_like(positions).astype(np.int)
    ax1 = run_loop_per_axis(positions[:, 0], velocities[:, 0])
    ax2 = run_loop_per_axis(positions[:, 1], velocities[:, 1])
    ax3 = run_loop_per_axis(positions[:, 2], velocities[:, 2])
    print(reduce(lambda a, b: a * b // gcd(a, b), [ax1, ax2, ax3]))


if __name__ == "__main__":
    sys.exit(main())