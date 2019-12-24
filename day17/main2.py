import sys
import numpy as np
from intcode import IntCodeComputer, parse_args


SCAFF = ord("#")
EMPTY = ord(".")

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


class ASCIIBot:
    def __init__(self, instructions):
        self.map = np.zeros((100, 100), dtype=np.int8)
        self.start = (0, 0)  # row, col
        # instructions[0] = 1  # part 1
        instructions[0] = 2  # part 2
        self.input_commands = []
        self.input_commands += self.movement_program()
        self.input_commands += [ord('n'), ord('\n')]
        print(self.input_commands)
        print([chr(x) for x in self.input_commands])
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
            if pixel_val in [ord("<"), ord(">"), ord("v"), ord("^")]:
                # where's the vacuum?
                self.start = (row_idx, col_idx)
            self.map[row_idx, col_idx] = pixel_val
            if col_idx > max_col:
                max_col = col_idx
            col_idx += 1
        self.map = self.map[:row_idx - 1, :max_col + 1]

    def get_intersection_map(self):
        align_map = self.map == 35
        align_map[1:, :] &= self.map[:-1, :] == 35
        align_map[:-1, :] &= self.map[1:, :] == 35
        align_map[:, 1:] &= self.map[:, :-1] == 35
        align_map[:, :-1] &= self.map[:, 1:] == 35
        return align_map

    def __str__(self):
        s = ""
        for row in self.map:
            s += "".join(chr(x) for x in row) + "\n"
        return s

    def movement_program(self):
        main_program = "A,A,B,C,B,C,B,C,A,C\n"
        func_a = """R,6,L,8,R,8\n"""
        func_b = """R,4,R,6,R,6,R,4,R,4\n"""
        func_c = """L,8,R,6,L,10,L,10\n"""
#         total = """
# R,6,L,8,R,8
# R,6,L,8,R,8
#
# R,4,R,6,R,6,R,4,R,4,
# L,8 R,6,L,10,L,10
#
# R,4,R,6,R,6,R,4,R,4,
# L,8,R,6,L,10,L,10
#
# R,4,R,6,R,6,R,4,R,4,
# L,8,R,6,L,10,L,10
#
# R,6,L,8,R,8
#
# L,8,R,6,L,10,L,10"""
        total = []
        def _to_intcode(insts):
            for x in insts:
                yield ord(x)
        total.extend(_to_intcode(main_program))
        total.extend(_to_intcode(func_a))
        total.extend(_to_intcode(func_b))
        total.extend(_to_intcode(func_c))
        return total

    def walk_scaffolding(self):
        curr_row, curr_col = self.start
        move_hor = False  # we check up/down first so False is OK
        while True:
            # we don't know which direction to face
            # and need to turn
            next_row, next_col = curr_row, curr_col
            # up
            if move_hor and curr_row - 1 >= 0 and self.map[curr_row - 1, curr_col] == SCAFF:
                next_row = curr_row - 1
                turn = 'L' if self.map[curr_row, curr_col] == ord('>') else 'R'
                move_hor = False
                movement = -1
            # down
            elif move_hor and curr_row + 1 <= self.map.shape[0] and self.map[curr_row + 1, curr_col] == SCAFF:
                next_row = curr_row + 1
                turn = 'R' if self.map[curr_row, curr_col] == ord('>') else 'L'
                move_hor = False
                movement = 1
            # left
            elif curr_col - 1 >= 0 and self.map[curr_row, curr_col - 1] == SCAFF:
                next_col = curr_col - 1
                turn = 'L' if self.map[curr_row, curr_col] == ord('^') else 'R'
                move_hor = True
                movement = -1
            # right
            elif curr_col + 1 <= self.map.shape[1] and self.map[curr_row, curr_col + 1] == SCAFF:
                next_col = curr_col + 1
                turn = 'R' if self.map[curr_row, curr_col] == ord('^') else 'L'
                move_hor = True
                movement = 1
            else:
                print("WE'RE DONE")
                break

            # how far do we go now
            while (0 <= next_row < self.map.shape[0] and
                   0 <= next_col < self.map.shape[1] and
                   self.map[next_row, next_col] == SCAFF):
                if move_hor:
                    next_col += movement
                else:
                    next_row += movement
            if move_hor:
                next_col -= movement
                count = abs(next_col - curr_col)
            else:
                next_row -= movement
                count = abs(next_row - curr_row)
            print("{},{}".format(turn, count))
            if move_hor:
                self.map[next_row, next_col] = ord("<") if movement < 0 else ord(">")
            else:
                self.map[next_row, next_col] = ord("^") if movement < 0 else ord("v")
            curr_row, curr_col = next_row, next_col


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    robot = ASCIIBot(instructions)
    # robot.walk_scaffolding()
    # print(robot)
    # print("Done with robot map")
    for output in robot.computer_gen:
        print(output)


if __name__ == "__main__":
    sys.exit(main())