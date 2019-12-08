import numpy as np

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6


def main():
    with open('input.txt') as img_text:
        img_data = np.array([int(x) for x in img_text.read().strip()])
    img_data = img_data.reshape((-1, IMAGE_HEIGHT, IMAGE_WIDTH))
    num_zeros = np.sum(img_data == 0, axis=(1, 2))
    layer = img_data[np.argmin(num_zeros)]
    print(np.sum(layer == 1) * np.sum(layer == 2))


if __name__ == "__main__":
    import sys
    sys.exit(main())