
from collections import defaultdict
import sys


def calc_indirect_orbits(orbited_to_orbiters, orbited, prev_orbits=0):
    if orbited not in orbited_to_orbiters:
        return prev_orbits - 1
    orbits = max(prev_orbits - 1, 0)
    for orbiter in orbited_to_orbiters[orbited]:
        orbits += calc_indirect_orbits(orbited_to_orbiters, orbiter, prev_orbits + 1)
    return orbits


def create_orbit_maps(orbit_map_lines):
    orbited_to_orbiters = defaultdict(list)
    orbiter_to_orbited = {}
    for line in orbit_map_lines:
        orbited, orbiter = line.strip().split(')')
        orbited_to_orbiters[orbited].append(orbiter)
        orbiter_to_orbited[orbiter] = orbited
    return orbited_to_orbiters, orbiter_to_orbited


def main():
    with open('input.txt') as orbit_map:
        orbited_to_orbiters, orbiter_to_orbited = create_orbit_maps(orbit_map)
    direct_orbits = len(orbiter_to_orbited)
    indirect_orbits = calc_indirect_orbits(orbited_to_orbiters, 'COM')
    print(direct_orbits, indirect_orbits, direct_orbits + indirect_orbits)


if __name__ == "__main__":
    sys.exit(main())