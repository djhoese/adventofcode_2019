import sys
import numpy as np
import random
from intcode import IntCodeComputer, parse_args


def patient_generator(growing_list, default=None):
    idx = 0
    while True:
        if idx >= len(growing_list):
            if default is not None:
                yield default
            continue
        val = growing_list[idx]
        if val is None:
            break
        idx += 1
        yield val


def next_position(curr_pos, prev_dir):
    adjust = 1 if prev_dir in [1, 2] else -1
    if prev_dir in [0, 2]:
        # print("Row change", curr_pos, prev_dir, adjust)
        curr_pos = (curr_pos[0] + adjust, curr_pos[1])
    else:
        # print("Column change", curr_pos, prev_dir, adjust)
        curr_pos = (curr_pos[0], curr_pos[1] + adjust)
    return curr_pos


def in_map(pos, shape):
    return 0 <= pos[0] < shape[0] and 0 <= pos[1] < shape[1]


def robot_dir(d):
    return {
        0: 1,
        1: 4,
        2: 2,
        3: 3,
    }[d]


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)

    ship_map = np.zeros((50, 50), dtype=np.int)
    start = (25, 25)  # row, col
    ship_map[start[0], start[1]] = 2  # been there
    curr_pos = start
    prev_dir = 0
    input_commands = [robot_dir(prev_dir)]
    stdin = patient_generator(input_commands)
    robot = IntCodeComputer(stdin=stdin, stdout=None)
    robot_gen = robot.run(instructions)
    status = next(robot_gen)
    step = 0
    while status != 2:
        # print("Next movement loop: ", status)
        # figure out where to go next
        if status == 0:
            next_pos = next_position(curr_pos, prev_dir)
            ship_map[next_pos[0], next_pos[1]] = -1  # wall
            # prev_dir = (prev_dir + 1) % 4
            # prev_dir = random.choice([x for x in [0, 1, 2, 3] if x != prev_dir])
        elif status == 1:
            curr_pos = next_position(curr_pos, prev_dir)
            ship_map[curr_pos[0], curr_pos[1]] = 2  # been there
            # keep going in the same direction if we haven't hit a wall yet
        else:
            raise ValueError("Unexpected status: ", status)

        possible_directions = []
        for possible_dir in [0, 1, 2, 3]:
            next_pos = next_position(curr_pos, possible_dir)
            print(curr_pos, possible_dir, next_pos, ship_map[next_pos[0], next_pos[1]])
            if in_map(next_pos, ship_map.shape) and ship_map[next_pos[0], next_pos[1]] in [0, 2]:
                possible_directions.append(possible_dir)
        if not possible_directions:
            ship_map[start[0], start[1]] = 5
            print(ship_map)
            return

        prev_dir = random.choice(possible_directions)
        input_commands.append(robot_dir(prev_dir))
        status = next(robot_gen)
        step += 1
        if step % 200000 == 0:
            ship_map[start[0], start[1]] = 6
            print(ship_map)
            return
    oxy_pos = next_position(curr_pos, prev_dir)
    ship_map[start[0], start[1]] = 9
    ship_map[oxy_pos[0], oxy_pos[1]] = 7
    print("Steps to find it: ", step, start, oxy_pos)
    print(ship_map)
    print("Fewest movements to oxygen: ", abs(oxy_pos[0] - start[0]) + abs(oxy_pos[1] - start[1]))


if __name__ == "__main__":
    sys.exit(main())