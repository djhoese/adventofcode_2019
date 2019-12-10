import sys
import numpy as np


def open_map(map_filename):
    map_list = []
    with open(map_filename, 'r') as map_file:
        for line in map_file:
            map_list.append(list(line.strip()))
    return np.array(map_list)


def get_visible_asteroids(asteroid_coords, base_asteroid_idx):
    x, y = asteroid_coords[base_asteroid_idx]
    # make a copy of the asteroids coordinates, relative to our location
    relative_coords = np.concatenate(
        [asteroid_coords[:base_asteroid_idx], asteroid_coords[base_asteroid_idx + 1:]])
    relative_coords[:, 0] -= x
    relative_coords[:, 1] -= y
    # calculate angle (radians) to our current position
    relative_angles = np.arctan2(relative_coords[:, 1], relative_coords[:, 0])
    unique_values, unique_indexes = np.unique(relative_angles, return_index=True)
    return unique_values, unique_indexes


def main():
    asteroid_map = open_map('input.txt')
    # asteroid_map = open_map('example1.txt')
    row_coords, col_coords = np.nonzero(asteroid_map == '#')
    # put "X" coords first, "Y" coords second
    asteroid_coords = np.array(list(zip(col_coords, row_coords)))

    # look at each asteroid
    total_visible = np.empty((asteroid_coords.shape[0],))
    for idx, asteroid_coord in enumerate(asteroid_coords):
        unique_values, unique_indexes = get_visible_asteroids(asteroid_coords, idx)
        total_visible[idx] = unique_values.size
    print(asteroid_coords[np.argmax(total_visible)], total_visible.max())


if __name__ == "__main__":
    sys.exit(main())