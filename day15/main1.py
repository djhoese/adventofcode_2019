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


class RepairDroid(object):
    def __init__(self, instructions):
        self.ship_map = np.zeros((50, 50), dtype=np.int)
        self.ship_map[:] = -1
        self.start = (25, 25)  # row, col
        self.ship_map[self.start[0], self.start[1]] = 0  # been there
        self.input_commands = []
        stdin = patient_generator(self.input_commands)
        self.robot = IntCodeComputer(stdin=stdin, stdout=None)
        self.robot_gen = self.robot.run(instructions)

    def reverse_direction(self, d):
        return {0: 2, 1: 3, 2: 0, 3:1}.get(d)

    def get_future_moves(self, curr_pos, num_steps, prev_dir):
        future_moves = []
        reverse_dir = self.reverse_direction(prev_dir)
        for possible_dir in [x for x in [0, 1, 2, 3] if x != reverse_dir]:
            next_pos = next_position(curr_pos, possible_dir)
            if not in_map(next_pos, self.ship_map.shape):
                # we would go off the array
                continue

            next_val = self.ship_map[next_pos[0], next_pos[1]]
            if next_val == -2:
                # known wall
                continue
            elif next_val != -1 and num_steps >= next_val:
                # we've been to this square before and didn't
                # get here faster
                continue
            future_moves.append(possible_dir)
        return future_moves

    def test_movement(self, curr_pos, directions):
        for direction in directions[:-1]:
            # we've already been to these spots, they better be valid
            self.input_commands.append(robot_dir(direction))
            next(self.robot_gen)
            curr_pos = next_position(curr_pos, direction)

        self.input_commands.append(robot_dir(directions[-1]))
        status = next(self.robot_gen)
        if status == 2:
            return len(directions)
        next_pos = next_position(curr_pos, directions[-1])
        if status == 0:
            # wall
            self.ship_map[next_pos[0], next_pos[1]] = -2  # wall
            future_moves = None
            directions = directions[:-1]  # cut off the last movement when we undo them
        elif status == 1:
            # did the movement
            self.ship_map[next_pos[0], next_pos[1]] = len(directions)
            future_moves = self.get_future_moves(next_pos, len(directions) + 1, directions[-1])

        # undo the movements we've done
        for direction in directions[::-1]:
            self.input_commands.append(robot_dir(self.reverse_direction(direction)))
            next(self.robot_gen)

        if future_moves is None:
            return None
        return [directions + [fm] for fm in future_moves]

    def search_for_position(self):
        curr_pos = self.start
        num_steps = 0
        loops_run = 0

        paths = [[x] for x in self.get_future_moves(curr_pos, num_steps, None)]
        while num_steps == 0:
            new_paths = []
            print(paths[0])
            for path in paths:
                result = self.test_movement(curr_pos, path)
                if result is None:
                    # hit a wall, couldn't go further
                    continue
                elif isinstance(result, list):
                    for fm in result:
                        new_paths.append(fm)
                else:
                    print("Found it!: ", result)
                    num_steps = result
                    break
            paths = new_paths
            loops_run += 1
            if loops_run % 10000 == 0:
                print(self.ship_map)
                break
        return num_steps


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    repair_droid = RepairDroid(instructions)
    print(repair_droid.search_for_position())


if __name__ == "__main__":
    sys.exit(main())