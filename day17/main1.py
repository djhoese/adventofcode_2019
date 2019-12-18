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


class VacuumRobot:
    def __init__(self, instructions):
        self.map = np.zeros((100, 100), dtype=np.int8)
        self.start = (0, 0)  # row, col
        self.input_commands = []
        stdin = patient_generator(self.input_commands)
        self.computer = IntCodeComputer(stdin=stdin, stdout=None)
        self.computer_gen = self.computer.run(instructions)

    def load_camera_image(self):
        row_idx = 0
        col_idx = 0
        max_col = 0
        for pixel_val in self.computer_gen:
            if pixel_val == 10:
                # new line
                row_idx += 1
                col_idx = 0
                continue
            self.map[row_idx, col_idx] = pixel_val
            if col_idx > max_col:
                max_col = col_idx
            col_idx += 1
        self.map = self.map[:row_idx - 1, :max_col]

    def get_intersection_map(self):
        align_map = self.map == 35
        align_map[1:, :] &= self.map[:-1, :] == 35
        align_map[:-1, :] &= self.map[1:, :] == 35
        align_map[:, 1:] &= self.map[:, :-1] == 35
        align_map[:, :-1] &= self.map[:, 1:] == 35
        return align_map


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    robot = VacuumRobot(instructions)
    robot.load_camera_image()
    align_map = robot.get_intersection_map()
    intersect_rows, intersect_cols = np.nonzero(align_map)
    print(np.sum(np.array(intersect_rows) * np.array(intersect_cols)))


if __name__ == "__main__":
    sys.exit(main())