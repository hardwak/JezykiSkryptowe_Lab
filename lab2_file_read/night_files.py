import sys


def night_files():
    hours = ['22', '23', '00', '01', '02', '03', '04', '05']
    for line in sys.stdin:
        parts = line.split()
        for hour in hours:
            if parts[3][-8:-6] == hour:
                print(parts)


if __name__ == "__main__":
    night_files()
