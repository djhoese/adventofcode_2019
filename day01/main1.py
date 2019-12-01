import numpy as np

input_data = np.loadtxt('input.txt')
print(int(np.sum(input_data // 3 - 2)))
