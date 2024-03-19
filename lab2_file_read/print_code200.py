import sys


def print_code200():
    for line in sys.stdin:
        parts = line.split()
        if parts[-2] == "200":
            print(parts)


if __name__ == "__main__":
    print_code200()
