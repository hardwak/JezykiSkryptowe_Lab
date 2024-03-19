import sys
import datetime


def friday_files():
    for line in sys.stdin:
        parts = line.split()
        timestamp = parts[3][1:]
        try:
            time = datetime.datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S')
            if time.weekday() == 4:
                print(parts)
        except ValueError:
            pass


if __name__ == "__main__":
    friday_files()
