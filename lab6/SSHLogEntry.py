from datetime import datetime
from ipaddress import IPv4Address
import re
import abc


class SSHLogEntry(abc.ABC):
    def __init__(self, date: datetime, name, pid: int, raw_message):
        self.date = date
        self.name = name
        self.pid = pid
        self._raw_message = raw_message

    def __str__(self):
        return self._raw_message

    def __repr__(self):
        return f"<SSHLogEntry> {self.date}, {self.name}, {self.pid} - {self._raw_message}"

    def __lt__(self, other):
        if isinstance(other, SSHLogEntry):
            return self.date < other.date
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, SSHLogEntry):
            return self.date > other.date
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, SSHLogEntry):
            return self.date == other.date and self.name == other.name and self.pid == other.pid
        else:
            return NotImplemented

    @property
    def raw_message(self):
        return self._raw_message

    def get_ip_v4_address(self):
        ipv4_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
        match = ipv4_pattern.search(self._raw_message)
        if match:
            return IPv4Address(match.group(0))
        else:
            return None

    @abc.abstractmethod
    def validate(self):
        pass

    @property
    def has_ip(self):
        if re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b').search(self._raw_message):
            return True
        else:
            return False


class SSHLogEntry_FailedPassword(SSHLogEntry):
    def __init__(self, date: datetime, name, pid: int, raw_message):
        failed_password_pattern = re.compile(r'\bFailed password\b')
        if not failed_password_pattern.search(raw_message):
            raise ValueError("This Log Entry do not represent an invalid password")

        super().__init__(date, name, pid, raw_message)

    def __str__(self):
        return f"Password failed for:\n{super().__str__()}"

    def validate(self):
        pattern = re.compile(
            r'(?P<date>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+'
            r'(?P<name>\S+)\s+'
            r'(?P<process>\S+)\[(?P<num>\d+)\]:\s+'
            r'(?P<message>.*)'
        )
        match = pattern.match(self._raw_message)
        data = match.groups()

        return (datetime.strptime(data[0], '%b %d %H:%M:%S') == self.date and
                data[2] == self.name and
                int(data[3]) == self.pid and
                data[4].startswith("Failed password"))


class SSHLogEntry_AcceptedPassword(SSHLogEntry):
    def __init__(self, date: datetime, name, pid: int, raw_message):
        accepted_password_pattern = re.compile(r'\bAccepted password\b')
        if not accepted_password_pattern.search(raw_message):
            raise ValueError("This Log Entry do not represent an accepted password")

        super().__init__(date, name, pid, raw_message)

    def __str__(self):
        return f"Password accepted for:\n{super().__str__()}"

    def validate(self):
        pattern = re.compile(
            r'(?P<date>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+'
            r'(?P<name>\S+)\s+'
            r'(?P<process>\S+)\[(?P<num>\d+)\]:\s+'
            r'(?P<message>.*)'
        )
        match = pattern.match(self._raw_message)
        data = match.groups()

        return (datetime.strptime(data[0], '%b %d %H:%M:%S') == self.date and
                data[2] == self.name and
                int(data[3]) == self.pid and
                data[4].startswith("Accepted password"))


class SSHLogEntry_Error(SSHLogEntry):
    def __init__(self, date: datetime, name, pid: int, raw_message):
        error_pattern = re.compile(r'\berror\b')
        if not error_pattern.search(raw_message):
            raise ValueError("This Log Entry do not represent an error")

        super().__init__(date, name, pid, raw_message)

    def __str__(self):
        return f"Error for:\n{super().__str__()}"

    def validate(self):
        pattern = re.compile(
            r'(?P<date>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+'
            r'(?P<name>\S+)\s+'
            r'(?P<process>\S+)\[(?P<num>\d+)\]:\s+'
            r'(?P<message>.*)'
        )
        match = pattern.match(self._raw_message)
        data = match.groups()

        return (datetime.strptime(data[0], '%b %d %H:%M:%S') == self.date and
                data[2] == self.name and
                int(data[3]) == self.pid and
                data[4].startswith("error:"))


class SSHLogEntry_Other(SSHLogEntry):
    def __init__(self, date: datetime, name, pid: int, raw_message):
        super().__init__(date, name, pid, raw_message)

    def __str__(self):
        return f"Other message:\n{super().__str__()}"

    def validate(self):
        return True
