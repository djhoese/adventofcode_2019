import sys
import numpy as np
from main1 import open_map, get_asteroid_angles


def main():
    # asteroid_map = open_map('example3.txt')
    # base_idx = 28
    # asteroid_map = open_map('example2.txt')
    # base_idx = 205
    asteroid_map = open_map('input.txt')
    base_idx = 170
    row_coords, col_coords = np.nonzero(asteroid_map == '#')
    # put "X" coords first, "Y" coords second
    asteroid_coords = np.array(list(zip(col_coords, row_coords)))

    # look at each asteroid
    num_destroyed = 0
    base_coords = asteroid_coords[base_idx]
    asteroid_coords = np.concatenate([[asteroid_coords[base_idx]], asteroid_coords[:base_idx], asteroid_coords[base_idx + 1:]])
    while num_destroyed < 200:
        asteroid_angles, asteroid_dist = get_asteroid_angles(asteroid_coords, 0)
        asteroid_angles = asteroid_angles[1:]
        asteroid_dist = asteroid_dist[1:]
        asteroid_info = [(idx, angle, dist) for idx, (angle, dist) in enumerate(zip(asteroid_angles, asteroid_dist))]
        asteroid_info = sorted(asteroid_info, key=lambda x: x[2])
        asteroid_indexes, asteroid_angles, asteroid_distances = zip(*asteroid_info)
        asteroid_angles = np.array(asteroid_angles)
        asteroid_coords = np.array([asteroid_coords[1:][x] for x in asteroid_indexes])
        # up is starting point and need to go clockwise
        # angles so far are -pi to pi
        asteroid_angles = 2 * np.pi - (asteroid_angles) - 1.5 * np.pi
        asteroid_angles[asteroid_angles < 0] += 2 * np.pi
        unique_values, unique_indexes = np.unique(asteroid_angles, return_index=True)
        destroy_order = np.argsort(unique_values)
        for unique_idx in destroy_order:
            orig_idx = unique_indexes[unique_idx]
            destroy_coord = asteroid_coords[orig_idx]
            num_destroyed += 1
            if num_destroyed == 200:
                print(destroy_coord[0] * 100 + destroy_coord[1])
        # remove destroyed asteroids
        asteroid_coords = np.concatenate([[base_coords], asteroid_coords[[x for x in range(asteroid_angles.shape[0]) if x not in unique_indexes]]])


if __name__ == "__main__":
    sys.exit(main())