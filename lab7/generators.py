import functools
import logging

import lab7.decorators as dec


def make_generator(func):
    n = 1
    while True:
        yield func(n)
        n += 1


@dec.log_func_decorator
def square(x):
    return x ** 2


def make_generator_mem(func):
    functools.cache(func)
    return make_generator(func)


@dec.log_object_created
class TestClass:
    def __init__(self):
        pass

    def do_something(self):
        print("do_something")


if __name__ == '__main__':
    gen = make_generator_mem(square)
    for _ in range(10):
        print(next(gen), end=' ')
    print()

    gen2 = make_generator(lambda x: x ** 2)
    for _ in range(10):
        print(next(gen2), end=' ')

    list_of_objects = []
    for _ in range(5):
        list_of_objects.append(TestClass())
