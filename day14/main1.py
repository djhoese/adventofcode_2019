import sys
import math


def read_mineral_maps(input_fn):
    min_to_ins = {}
    min_to_production = {}
    with open(input_fn, 'r') as input_file:
        for line in input_file:
            inputs, output = line.strip().split(' => ')
            inputs = [x.strip().split(' ') for x in inputs.split(',')]
            inputs = [(int(x[0]), x[1]) for x in inputs]
            output = output.split(' ')
            min_to_production[output[1]] = int(output[0])
            min_to_ins[output[1]] = inputs
    return min_to_ins, min_to_production


def calc_ore(min_to_ins, min_to_production, mineral, num_needed, total_produced=None, total_needed=None):
    if total_produced is None:
        total_produced = {}
        total_needed = {}

    # how much do we need total
    total_needed[mineral] = total_needed.get(mineral, 0) + num_needed
    # how much "extra" do we have from previous production
    diff = total_needed.setdefault(mineral, 0) - total_produced.setdefault(mineral, 0)
    if diff < 0:
        # we already have what is needed
        diff = 0
    times_to_produce = math.ceil(diff / min_to_production[mineral])
    for num_in, mineral_in in min_to_ins.get(mineral, []):
        if mineral_in == 'ORE':
            total_needed[mineral_in] = total_needed.get(mineral_in, 0) + math.floor(num_needed / min_to_production[mineral]) * num_in
            total_produced[mineral_in] = total_produced.get(mineral_in, 0) + num_in * times_to_produce
            continue
        num_in *= times_to_produce
        calc_ore(min_to_ins, min_to_production, mineral_in, num_in, total_produced, total_needed)

    total_produced[mineral] = total_produced.get(mineral, 0) + min_to_production[mineral] * times_to_produce
    return total_produced, total_needed


def main():
    min_to_ins, min_to_production = read_mineral_maps('input.txt')
    min_to_production['ORE'] = 1
    input_ore = 1000000000000
    total_fuel = 1
    total_produced, total_needed = calc_ore(min_to_ins, min_to_production, 'FUEL', 1)
    print(total_produced['ORE'])  # part 1
    fuel_step = 1000000
    tp = total_produced.copy()
    tn = total_needed.copy()
    while tp['ORE'] < input_ore:
        calc_ore(min_to_ins, min_to_production, 'FUEL', fuel_step, total_produced=tp, total_needed=tn)
        total_fuel += fuel_step
        if tp['ORE'] > (input_ore - total_produced['ORE'] * 10000):
            fuel_step = 1
        elif tp['ORE'] > (input_ore - total_produced['ORE'] * 1000000):
            fuel_step = 100
        elif tp['ORE'] > (input_ore - total_produced['ORE'] * 10000000):
            fuel_step = 1000
    print(total_fuel - 1)  # part 2 - WTF


if __name__ == "__main__":
    sys.exit(main())