import string
import random


class PasswordGenerator:
    def __init__(self, length, charset, count):
        self.length = length
        self.charset = charset
        self.count = count
        self.generated = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.generated >= self.count:
            raise StopIteration
        self.generated += 1
        return ''.join(random.choice(self.charset) for _ in range(self.length))


if __name__ == '__main__':
    password = PasswordGenerator(8, string.ascii_letters, 5)
    print(next(password))
    print(next(password))

    for passw in password:
        print(passw)

    print(next(password))
