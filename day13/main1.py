import sys
import numpy as np
from intcode import IntCodeComputer, parse_args
from itertools import repeat
import select
from time import sleep


CANVAS_SYMBOLS = {
    0: ' ',
    1: '|',
    2: '#',
    3: '-',
    4: '*',
}


KEY_MAP = {
    '\x1b[D': -1,
    '-1': -1,
    '\x1b[C': 1,
    '1': 1,
    '\x1b[B': 0,
    '0': 0,
}


def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            # escape sequence
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def patient_generator(growing_list, default=None):
    idx = 0
    while True:
        if idx >= len(growing_list):
            if default is not None:
                yield KEY_MAP[getch()]
                # yield KEY_MAP[input("Controller: ")]
                # print("Yielding default")
                # yield default
            continue
        val = growing_list[idx]
        if val is None:
            break
        idx += 1
        yield val


def run_game(instructions):
    # tokens = 0  # part 1
    tokens = 2  # part 2

    controller = [0]
    stdin = patient_generator(controller, default=0)
    computer = IntCodeComputer(stdin=stdin, stdout=None)
    # insert token
    instructions[0] = tokens
    comp_gen = computer.run(instructions)
    rows = 22
    cols = 35
    game_canvas = np.zeros((rows, cols))
    canvas_row = "{}" * cols
    num_blocks = 0
    x_pos = next(comp_gen)
    y_pos = next(comp_gen)
    tile_id = next(comp_gen)

    while True:
        if x_pos == -1 and y_pos == 0:
            print("Score: ", tile_id)
        else:
            game_canvas[y_pos, x_pos] = tile_id
            num_blocks += int(tile_id == 2)

            for row in game_canvas:
                print(canvas_row.format(*(CANVAS_SYMBOLS[x] for x in row)))

        x_pos = next(comp_gen, None)
        y_pos = next(comp_gen, None)
        tile_id = next(comp_gen, None)
        if tile_id is None:
            print("Tile ID is None")
            break
        # sleep(0.01)
    # print(num_blocks)  # part 1


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    run_game(instructions)


if __name__ == "__main__":
    sys.exit(main())