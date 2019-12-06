
import sys
from main1 import create_orbit_maps


def orbit_chain(orbiter_to_orbited, orbiter, dst='COM'):
    curr_orbited = orbiter
    while curr_orbited != dst:
        curr_orbited = orbiter_to_orbited[curr_orbited]
        yield curr_orbited


def main():
    with open('input.txt') as orbit_map:
        orbited_to_orbiters, orbiter_to_orbited = create_orbit_maps(orbit_map)
    you_chain = list(orbit_chain(orbiter_to_orbited, 'YOU'))
    san_chain = list(orbit_chain(orbiter_to_orbited, 'SAN'))
    for orbited in you_chain:
        if orbited in san_chain:
            break
    print(you_chain.index(orbited) + san_chain.index(orbited))



if __name__ == "__main__":
    sys.exit(main())