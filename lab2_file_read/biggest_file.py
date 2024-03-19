import sys


def biggest_file():
    biggest = {}
    biggest_size = 0

    for line in sys.stdin:
        parts = line.split()
        try:
            if int(parts[-1]) > biggest_size:
                biggest_size = int(parts[-1])
                biggest = parts
        except ValueError:
            pass
    print("Size of biggest file: " + str(biggest_size))
    print("Path of biggest file: " + str(biggest[6]))


if __name__ == "__main__":
    biggest_file()