import sys


def polish_files():
    for line in sys.stdin:
        parts = line.split()
        if parts[0].endswith('.pl'):
            print(parts)


if __name__ == "__main__":
    polish_files()