import sys
import numpy as np


def open_map(map_filename):
    map_list = []
    with open(map_filename, 'r') as map_file:
        for line in map_file:
            map_list.append(list(line.strip()))
    return np.array(map_list)


def get_asteroid_angles(asteroid_coords, base_asteroid_idx):
    x, y = asteroid_coords[base_asteroid_idx]
    # make a copy of the asteroids coordinates, relative to our location
    # relative_coords = np.concatenate(
    #     [asteroid_coords[:base_asteroid_idx], asteroid_coords[base_asteroid_idx + 1:]])
    relative_coords = asteroid_coords.copy()
    relative_coords[:, 0] -= x
    relative_coords[:, 1] = y - relative_coords[:, 1]
    # calculate angle (radians) to our current position
    relative_angles = np.arctan2(relative_coords[:, 1], relative_coords[:, 0])
    asteroid_distance = np.sqrt(relative_coords[:, 0]**2 + relative_coords[:, 1]**2)
    return relative_angles, asteroid_distance


def main():
    asteroid_map = open_map('input.txt')
    asteroid_map = open_map('example2.txt')
    row_coords, col_coords = np.nonzero(asteroid_map == '#')
    # put "X" coords first, "Y" coords second
    asteroid_coords = np.array(list(zip(col_coords, row_coords)))

    # look at each asteroid
    total_visible = np.empty((asteroid_coords.shape[0],))
    for idx in range(asteroid_coords.shape[0]):
        relative_angles = get_asteroid_angles(asteroid_coords, idx)[0]
        relative_angles = np.concatenate(
            [relative_angles[:idx], relative_angles[idx + 1:]]
        )
        unique_values = np.unique(relative_angles)
        total_visible[idx] = unique_values.size
    max_idx = np.argmax(total_visible)
    print(max_idx, asteroid_coords[max_idx], total_visible[max_idx])


if __name__ == "__main__":
    sys.exit(main())