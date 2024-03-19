import sys


def gigabytes_received():
    bytesReceived = 0

    for line in sys.stdin:
        parts = line.split()
        try:
            bytesReceived += int(parts[-1])
        except ValueError:
            pass
    print("Gigabytes received: {}".format(bytesReceived / 10 ** 9))


if __name__ == "__main__":
    gigabytes_received()