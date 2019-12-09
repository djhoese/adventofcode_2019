import sys
import numpy as np
import logging

LOG = logging.getLogger(__name__)


class IntCodeComputer(object):
    def __init__(self, stdin=sys.stdin, stdout=sys.stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.relative_base_reg = 0
        self.memory = None
        self.ip = 0

    def apply_error_code(self, noun=None, verb=None):
        if noun is not None:
            self.memory[1] = noun
        if verb is not None:
            self.memory[2] = verb

    def get_address(self, param_modes, num_args, offset=0):
        for i in range(num_args):
            if param_modes[i] == 0:
                LOG.debug("Argument {}: Absolute Position".format(i))
                yield self.memory[self.ip + offset + i + 1]
            elif param_modes[i] == 1:
                LOG.debug("Argument {}: Immediate".format(i))
                yield self.ip + offset + i + 1
            elif param_modes[i] == 2:
                LOG.debug("Argument {}: Relative".format(i))
                yield self.relative_base_reg + self.memory[self.ip + offset + i + 1]
            else:
                raise RuntimeError("Unknown parameter mode: {}".format(param_modes[i]))

    def get_args(self, param_modes, num_args):
        for i in range(num_args):
            if param_modes[i] == 0:
                LOG.debug("Argument {}: Absolute Position".format(i))
                yield self.memory[self.memory[self.ip + i + 1]]
            elif param_modes[i] == 1:
                LOG.debug("Argument {}: Immediate".format(i))
                yield self.memory[self.ip + i + 1]
            elif param_modes[i] == 2:
                LOG.debug("Argument {}: Relative".format(i))
                yield self.memory[self.relative_base_reg + self.memory[self.ip + i + 1]]
            else:
                raise RuntimeError("Unknown parameter mode: {}".format(param_modes[i]))

    def run(self, instructions):
        if self.memory is None:
            self.memory = np.zeros(instructions.size * 20, dtype=np.int64)
        else:
            raise NotImplementedError("Can't run new instructions on the same computer")
        self.memory[:instructions.size] = instructions
        LOG.debug("Memory size: {}".format(self.memory.shape))
        LOG.debug("Instruction size: {}".format(instructions.shape))
        np.set_printoptions(edgeitems=50, linewidth=200)

        cycle_count = -1
        while True:
            cycle_count += 1
            # if cycle_count > 90:
            #     break
            opcode = self.memory[self.ip]
            LOG.debug("Opcode: {:>5d} | Instruction Pointer: {:>5d} | Relative Base Register: {:>10d}".format(
                opcode, self.ip, self.relative_base_reg))
            opcode = f"{opcode:05d}"
            param_modes = [int(x) for x in reversed(opcode[:-2])]
            opcode = int(opcode[-2:])

            if opcode == 1:
                # ADD
                arg1, arg2 = self.get_args(param_modes, 2)
                # dst = self.memory[self.ip + 3]
                dst, = self.get_address(param_modes[2:], 1, offset=2)
                LOG.debug("Add: {} + {} => *{}".format(arg1, arg2, dst))
                self.memory[dst] = arg1 + arg2
                self.ip += 4
            elif opcode == 2:
                # MULT
                arg1, arg2 = self.get_args(param_modes, 2)
                # dst = self.memory[self.ip + 3]
                dst, = self.get_address(param_modes[2:], 1, offset=2)
                self.memory[dst] = arg1 * arg2
                self.ip += 4
            elif opcode == 3:
                # STDIN
                if self.stdin is sys.stdin:
                    print("Enter single digit: ")
                user_input = int(next(self.stdin))
                dst, = self.get_address(param_modes, 1)
                # dst = self.memory[self.ip + 1]
                self.memory[dst] = user_input
                self.ip += 2
            elif opcode == 4:
                # STDOUT
                arg1, = self.get_args(param_modes, 1)
                if hasattr(self.stdout, 'write'):
                    LOG.debug("Printing...")
                    print(arg1, file=self.stdout)
                yield arg1
                self.ip += 2
            elif opcode == 5:
                # JMPT
                arg1, arg2 = self.get_args(param_modes, 2)
                if arg1:
                    self.ip = arg2
                else:
                    self.ip += 3
            elif opcode == 6:
                # JMPF
                arg1, arg2 = self.get_args(param_modes, 2)
                if arg1 == 0:
                    self.ip = arg2
                else:
                    self.ip += 3
            elif opcode == 7:
                # LT
                arg1, arg2 = self.get_args(param_modes, 2)
                # dst = self.memory[self.ip + 3]
                dst, = self.get_address(param_modes[2:], 1, offset=2)
                self.memory[dst] = int(arg1 < arg2)
                self.ip += 4
            elif opcode == 8:
                # EQ
                arg1, arg2 = self.get_args(param_modes, 2)
                # dst = self.memory[self.ip + 3]
                dst, = self.get_address(param_modes[2:], 1, offset=2)
                LOG.debug("Equal: {} == {} => *{}".format(arg1, arg2, dst))
                self.memory[dst] = int(arg1 == arg2)
                self.ip += 4
            elif opcode == 9:
                # REL BASE
                arg1, = self.get_args(param_modes, 1)
                self.relative_base_reg += arg1
                self.ip += 2
            elif opcode == 99:
                return self.memory[0]
            else:
                raise ValueError(f"Unknown opcode: {opcode}")


def parse_args():
    import os
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help="Log level (ERROR-WARNING-INFO-DEBUG)")
    parser.add_argument('instructions', nargs='?',
                        help="File or raw instructions to run")
    args = parser.parse_args()

    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=levels[min(args.verbosity, 3)])

    if args.instructions and os.path.isfile(args.instructions):
        file_in = args.instructions
    elif args.instructions:
        # raw code
        file_in = [bytes(args.instructions, 'utf8')]
    else:
        file_in = 'input.csv'

    return args, file_in


if __name__ == "__main__":
    args, file_in = parse_args()
    instructions = np.loadtxt(file_in, delimiter=',', dtype=np.int)
    comp = IntCodeComputer()
    list(comp.run(instructions))
