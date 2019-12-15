import sys
import numpy as np
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
        self.ship_map = np.zeros((41, 41), dtype=np.int)
        self.ship_map[:] = -1
        self.start = (21, 21)  # row, col
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

    def test_movement(self, curr_pos, base_path, directions):
        for direction in directions[:-1]:
            # we've already been to these spots, they better be valid
            self.input_commands.append(robot_dir(direction))
            next(self.robot_gen)
            curr_pos = next_position(curr_pos, direction)

        self.input_commands.append(robot_dir(directions[-1]))
        status = next(self.robot_gen)
        next_pos = next_position(curr_pos, directions[-1])
        if status == 0:
            # wall
            self.ship_map[next_pos[0], next_pos[1]] = -2  # wall
            future_moves = None
            directions = directions[:-1]  # cut off the last movement when we undo them
        elif status in [1, 2]:
            # did the movement
            self.ship_map[next_pos[0], next_pos[1]] = len(base_path) + len(directions)
            future_moves = self.get_future_moves(next_pos, len(base_path) + len(directions) + 1, directions[-1])

        # undo the movements we've done
        for direction in directions[::-1]:
            self.input_commands.append(robot_dir(self.reverse_direction(direction)))
            next(self.robot_gen)

        if future_moves is None and status != 2:
            return None, status == 2
        return [directions + [fm] for fm in future_moves], status == 2

    def search_for_position(self):
        curr_pos = self.start
        num_steps = 0
        loops_run = 0

        paths = [[x] for x in self.get_future_moves(curr_pos, num_steps, None)]
        base_path = []
        oxy_path = None
        while paths:
            new_paths = []
            for path in paths:
                result, found_it = self.test_movement(curr_pos, base_path, path)
                if result is None:
                    # hit a wall, couldn't go further
                    # the wall is the last element of the path
                    continue
                elif isinstance(result, list):
                    if found_it:
                        oxy_path = base_path + path
                        num_steps = len(oxy_path)  # part 1
                        for fm in result:
                            new_paths.append(fm)
                    else:
                        for fm in result:
                            new_paths.append(fm)
            # shorten how far each path has to go
            idx = 0
            if not new_paths:
                # we have nothing else to look for
                print("Done")
                break
            if len(new_paths) > 1:
                while all([p[:idx] == new_paths[0][:idx] for p in new_paths[1:]]):
                    idx += 1
                idx -= 1
            new_base = new_paths[0][:idx]
            base_path += new_base
            new_paths = [p[idx:] for p in new_paths]
            paths = new_paths
            loops_run += 1

            # the drone is back where this loop started, we have to move it to base path
            for path_elem in new_base:
                self.input_commands.append(robot_dir(path_elem))
                next(self.robot_gen)
                curr_pos = next_position(curr_pos, path_elem)
            if not in_map(curr_pos, self.ship_map.shape):
                raise RuntimeError("We are outside the map!")
        idx = 0
        long_path = base_path + paths[0]
        while oxy_path[:idx] == long_path[:idx]:
            idx += 1
        idx -= 1
        longest_oxy_fill = len(oxy_path[idx:]) + len(long_path[idx:])
        print(longest_oxy_fill)  # part 2
        return num_steps


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    repair_droid = RepairDroid(instructions)
    print(repair_droid.search_for_position())


if __name__ == "__main__":
    sys.exit(main())