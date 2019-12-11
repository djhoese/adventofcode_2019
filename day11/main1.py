import sys
import numpy as np
from intcode import IntCodeComputer, parse_args


def patient_generator(growing_list):
    idx = 0
    while True:
        if idx >= len(growing_list):
            continue
        val = growing_list[idx]
        if val is None:
            break
        idx += 1
        yield val


class Robot:
    def __init__(self, initial_panel=0, initial_pos=(50, 50), grid_size=(100, 100)):
        # row, col
        self._pos = initial_pos
        # 0 = up
        # 1 = right
        # 2 = down
        # 3 = left
        self._dir = 0  # up
        self.grid_size = grid_size
        self.grid_state = np.zeros(grid_size, dtype=np.uint8)
        self.grid_painted = np.zeros(grid_size)
        self.grid_state[self._pos[0], self._pos[1]] = initial_panel
        self._stdin_colors = [self.grid_state[self._pos[0], self._pos[1]]]
        self._stdin = patient_generator(self._stdin_colors)
        self.computer = IntCodeComputer(stdin=self._stdin)
        self.panels_painted = 0

    def run(self, instructions):
        computer_gen = self.computer.run(instructions)
        for color_to_paint in computer_gen:
            # paint
            self.grid_state[self._pos[0], self._pos[1]] = color_to_paint
            if self.grid_painted[self._pos[0], self._pos[1]] == 0:
                self.grid_painted[self._pos[0], self._pos[1]] = 1
                self.panels_painted += 1

            # move
            turn_to_make = next(computer_gen)
            self._dir += 1 if turn_to_make == 1 else -1
            self._dir = self._dir % 4
            if self._dir in [0, 2]:
                # row is 0 at top
                mov = 1 if self._dir == 2 else -1
                # row, col
                self._pos = (self._pos[0] + mov, self._pos[1])
            elif self._dir in [1, 3]:
                mov = -1 if self._dir == 3 else 1
                self._pos = (self._pos[0], self._pos[1] + mov)
            else:
                raise RuntimeError("WTF Direction is {}!".format(self._dir))
            self._stdin_colors.append(self.grid_state[self._pos[0], self._pos[1]])


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    # robot = Robot(grid_size=(100, 100), initial_pos=(50, 50), initial_panel=0)  # part 1
    robot = Robot(grid_size=(10, 48), initial_pos=(0, 5), initial_panel=1)  # part 2
    robot.run(instructions)
    print(robot.panels_painted)  # part 1
    print(robot.grid_state)  # part 2


if __name__ == "__main__":
    sys.exit(main())