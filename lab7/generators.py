import functools

from lab7.decorators import log_func_decorator


def make_generator(func):
    n = 1
    while True:
        yield func(n)
        n += 1


@log_func_decorator
def square(x):
    return x ** 2


def make_generator_mem(func):
    functools.cache(func)
    return make_generator(func)


if __name__ == '__main__':
    gen = make_generator_mem(square)
    for _ in range(10):
        print(next(gen), end=' ')
    print()

    gen2 = make_generator(lambda x: x ** 2)
    for _ in range(10):
        print(next(gen2), end=' ')
