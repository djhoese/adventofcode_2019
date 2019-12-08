import numpy as np

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6


def main():
    with open('input.txt') as img_text:
        img_data = np.array([int(x) for x in img_text.read().strip()], dtype=np.uint8)
    img_data = img_data.reshape((-1, IMAGE_HEIGHT, IMAGE_WIDTH))
    final_img = np.ones((IMAGE_HEIGHT, IMAGE_WIDTH), np.uint8) * 2  # init to transparent
    for layer in img_data:
        mask = final_img == 2
        final_img[mask] = layer[mask]
    print(final_img)


if __name__ == "__main__":
    import sys
    sys.exit(main())