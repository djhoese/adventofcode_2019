import numpy as np


def movement_to_line(movements):
    """Convert R/L/U/D movements to line positions starting from (0, 0)."""
    curr_x = 0
    curr_y = 0
    coords = [(curr_x, curr_y)]
    for movement in movements:
        direction = movement[0]
        count = int(movement[1:])
        if direction in ('L', 'D'):
            count *= -1
        if direction in ('L', 'R'):
            curr_x += count
        else:
            curr_y += count
        coords.append((curr_x, curr_y))
    return np.array(coords)


def movement_to_points(movements):
    """Convert R/L/U/D movements to point positions starting from (0, 0)."""
    curr_x = 0
    curr_y = 0
    coords = []
    for movement in movements:
        direction = movement[0]
        count = int(movement[1:])
        offset = -1 if direction in ('L', 'D') else 1
        while count > 0:
            if direction in ('L', 'R'):
                curr_x += offset
            else:
                curr_y += offset
            coords.append((curr_x, curr_y))
            count -= 1
    return coords


def points_intersect(points1, points2):
    """Get coordinates that appear in both sets of points."""


def main():
    movements = np.loadtxt('input.csv', delimiter=',', dtype=str)
    wire1_movements = movements[0]
    wire2_movements = movements[1]
    wire1_points = movement_to_points(wire1_movements)
    wire2_points = movement_to_points(wire2_movements)
    wire1_set = set(wire1_points)
    wire2_set = set(wire2_points)
    intersect_points = wire1_set & wire2_set
    distance = [abs(x) + abs(y) for x, y in intersect_points]
    print(min(distance))


if __name__ == "__main__":
    import sys
    sys.exit(main())
