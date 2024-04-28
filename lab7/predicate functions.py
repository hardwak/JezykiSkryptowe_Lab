def forall(predicate, iterable):
    for element in iterable:
        if not predicate(element):
            return False
    return True


def exists(predicate, iterable):
    for element in iterable:
        if predicate(element):
            return True

    return False


def atleast(n, predicate, iterable):
    count = 0
    for element in iterable:
        if predicate(element):
            count += 1

    return count >= n


def atmost(n, predicate, iterable):
    count = 0
    for element in iterable:
        if predicate(element):
            count += 1

    return count <= n and count != 0


if __name__ == '__main__':
    print(atmost(2, lambda x: x > 4, [1, 2, 3, 4, 5]))
