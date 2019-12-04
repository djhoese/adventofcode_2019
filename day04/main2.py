import sys
from collections import Counter

START = 359282
END = 820401


def main():
    count = 0
    start_tuple = tuple(int(x) for x in str(START))
    end_tuple = tuple(int(x) for x in str(END))
    # for loop for each digit
    for d1 in range(start_tuple[0], end_tuple[0] + 1):
        for d2 in range(d1, 10):
            for d3 in range(d2, 10):
                for d4 in range(d3, 10):
                    for d5 in range(d4, 10):
                        for d6 in range(d5, 10):
                            num_tuple = (d1, d2, d3, d4, d5, d6)
                            if num_tuple < start_tuple or num_tuple > end_tuple:
                                break
                            c = set(Counter(num_tuple).values())
                            if c & {2}:
                                count += 1

    print(count)


if __name__ == "__main__":
    sys.exit(main())