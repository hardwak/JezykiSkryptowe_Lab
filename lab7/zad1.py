import statistics


def acronym(words):
    return ''.join(map(lambda word: word[0].upper(), words))


def median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    return sorted_numbers[(n - 1) // 2]


def root_square_newton(x, epsilon):
    def newton_iteration(y):
        next_y = (y + x / y) / 2
        return next_y if abs(next_y - y) < epsilon else newton_iteration(next_y)

    initial_guess = x / 2
    return newton_iteration(initial_guess)


def make_alpha_dict(text):
    words = text.split()
    alpha_dict = {}

    def add_to_dict(word):
        unique_chars = set(word)

        def add_char(char):
            alpha_dict[char] = alpha_dict[char] + [word] if char in alpha_dict else [word]

        list(map(add_char, unique_chars))

    list(map(add_to_dict, words))
    return alpha_dict


def flatten(lst):
    return [subitem for item in lst
            for subitem in (flatten(item) if isinstance(item, list) else [item])]


if __name__ == '__main__':
    print(acronym(["asdf", "sdfg", "qeq", "ert"]))
    print(median([1, 1, 19, 2, 3, 4, 4, 5, 1]))
    print(make_alpha_dict('on i ona'))
    print(flatten([1, [2, 3], [[4, 5], 6]]))
