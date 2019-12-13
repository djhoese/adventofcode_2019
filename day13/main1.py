import sys
import numpy as np
from intcode import IntCodeComputer, parse_args
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
                if default is sys.stdin:
                    yield KEY_MAP[getch()]
                else:
                    yield default
            continue
        val = growing_list[idx]
        if val is None:
            break
        idx += 1
        yield val


def run_game(instructions):
    # tokens = 0  # part 1
    tokens = 2  # part 2
    human = False

    controller = [0]
    stdin = patient_generator(controller, default=sys.stdin if human else 0)
    computer = IntCodeComputer(stdin=stdin, stdout=None)
    if tokens:
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
    paddle = (0, 0)
    sleep_time = 0.0
    score_str = ""

    while True:
        if x_pos == -1 and y_pos == 0:
            score_str = f"Score: {tile_id:d}"
        else:
            game_canvas[y_pos, x_pos] = tile_id
            num_blocks += int(tile_id == 2)
            if tile_id == 4:
                # ball
                if paddle[1] != x_pos and y_pos < paddle[0]:
                    controller.append(1 if paddle[1] < x_pos else -1)
            elif tile_id == 3:
                paddle = (y_pos, x_pos)
                sleep_time = 0.05

            if human:
                for row in game_canvas:
                    print(canvas_row.format(*(CANVAS_SYMBOLS[x] for x in row)))
                print(score_str)

        x_pos = next(comp_gen, None)
        y_pos = next(comp_gen, None)
        tile_id = next(comp_gen, None)
        if tile_id is None:
            break
        if human:
            sleep(sleep_time)
    if tokens:
        print(score_str)  # part 2
    else:
        print(num_blocks)  # part 1


def main():
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    run_game(instructions)


if __name__ == "__main__":
    sys.exit(main())