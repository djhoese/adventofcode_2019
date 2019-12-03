import numpy as np
from main1 import movement_to_points

TEST_MOVEMENTS1 = [
    ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
    ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"]
]


def main():
    movements = np.loadtxt('input.csv', delimiter=',', dtype=str)
    wire1_movements = movements[0]
    wire2_movements = movements[1]
    wire1_points = movement_to_points(wire1_movements)
    wire2_points = movement_to_points(wire2_movements)
    wire1_set = set(wire1_points)
    wire2_set = set(wire2_points)
    intersect_points = list(wire1_set & wire2_set)

    all_steps = []
    for ipoint in intersect_points:
        # add 1 because we didn't include the origin
        wire1_steps = wire1_points.index(ipoint) + 1
        wire2_steps = wire2_points.index(ipoint) + 1
        all_steps.append(wire1_steps + wire2_steps)
    print(min(all_steps))


if __name__ == "__main__":
    import sys
    sys.exit(main())
