import sys

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
                            count += any([d1 == d2, d2 == d3, d3 == d4, d4 == d5, d5 == d6])
    print(count)


if __name__ == "__main__":
    sys.exit(main())