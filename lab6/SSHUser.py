import re


class SSHUser:
    def __init__(self, username, last_login):
        self.username = username
        self.last_login = last_login

    def validate(self):
        pattern = re.compile(r'^[a-z_][a-z0-9_-]{0,31}$')
        return pattern.match(self.username) is not None
