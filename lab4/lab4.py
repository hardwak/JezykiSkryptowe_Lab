import os
import sys


def print_filtered_env_vars():
    osVars = sorted(os.environ.items())
    for var in osVars:
        print(var)
    for var in sys.argv:
        print(var)


def print_PATH_vars():
    for path in os.environ["PATH"].split(os.pathsep):
        print(path)


def print_PATH_vars_and_files():
    for path in os.environ["PATH"].split(os.pathsep):
        print(path)
        for filename in os.listdir(path):
            print(filename)


def my_own_tail():
    lines = 10
    linesArgument = False
    if sys.argv[1].startswith("--lines="):
        lines = int(sys.argv[1].split("=")[1])
        linesArgument = True

    filepath = str(sys.argv[1])
    if linesArgument:
        filepath = str(sys.argv[2])

    with open(filepath, 'r') as f:
        content = f.readlines()[-lines:]
        for line in content:
            print(line)




if __name__ == '__main__':
    print_filtered_env_vars()
