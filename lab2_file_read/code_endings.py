import sys


def code_endings():
    code200, code302, code404, sum = 0, 0, 0, 0

    for line in sys.stdin:
        parts = line.split()
        sum += 1
        if parts[-2] == "200":
            code200 += 1
        elif parts[-2] == "302":
            code302 += 1
        elif parts[-2] == "404":
            code404 += 1

    print("Code200: {}".format(code200))
    print("Code302: {}".format(code302))
    print("Code404: {}".format(code404))
    print("Sum: {}".format(sum))
    print("Another Codes: {}".format(sum - code200 - code302 - code404))


if __name__ == "__main__":
    code_endings()
