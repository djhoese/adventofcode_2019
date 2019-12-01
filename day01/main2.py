import numpy as np

input_data = np.loadtxt('input.txt')
def get_fuel_fuel(x):
    if np.all(x <= 0):
        return 0
    fuel_needed = np.maximum(x // 3 - 2, 0)
    return fuel_needed + get_fuel_fuel(fuel_needed)
print(int(np.sum(get_fuel_fuel(input_data))))
