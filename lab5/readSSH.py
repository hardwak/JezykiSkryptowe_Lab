import re
import sys
import logging
from collections import namedtuple
from datetime import datetime
import random

log = namedtuple('log', ['date', 'name', 'num', 'message'])

logger = logging.getLogger(__name__)
logging.basicConfig(filename='readSSH.log', level=logging.INFO)


def read_ssh_logs(filename):
    entries = []
    with open(filename, 'r') as file:
        for line in file:
            entry = parse_line(line)
            entries.append(entry)

    return entries


def parse_line(line):
    pattern = re.compile(
        r'(?P<date>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+'
        r'(?P<name>\S+)\s+'
        r'(?P<num>\S+\[\d+\]):\s+'
        r'(?P<message>.*)'
    )

    match = pattern.match(line)
    data = match.groups()
    date = datetime.strptime(data[0], '%b %d %H:%M:%S').strftime('2023-%m-%d %H:%M:%S')
    name = data[1]
    num = data[2]
    message = data[3]

    return log(date, name, num, message)

    # if sys.argv[1] == "tuple":
    #     data = match.groups()
    #     date = datetime.strptime(data[0], '%b %d %H:%M:%S').strftime('2023-%m-%d %H:%M:%S')
    #     name = data[1]
    #     num = data[2]
    #     message = data[3]
    #
    #     return log(date, name, num, message)
    # elif sys.argv[1] == "dictionary":
    #     data = match.groupdict()
    #     log_dict = {
    #         "date": datetime.strptime(data.get("date"), '%b %d %H:%M:%S').strftime('2023-%m-%d %H:%M:%S'),
    #         "name": data.get("name"),
    #         "num": data.get("num"),
    #         "message": data.get("message")
    #     }
    #     return log_dict
    # else:
    #     raise ValueError("Choose a valid 'tuple' or 'dictionary'")


def get_ipv4s_from_log(entry):
    ipv4_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')

    addresses = ipv4_pattern.findall(entry.message)
    return addresses


def get_user_from_log(entry):
    user_pattern = re.compile(r'\buser=\S+\b')
    match = user_pattern.search(entry.message)
    if match:
        return match.group()[5:]
    else:
        return None


def get_message_type(entry):
    successful_login_pattern = re.compile(r'Accepted password')
    failed_login_pattern = re.compile(r'authentication failure')
    connection_closed_pattern = re.compile(r'Connection closed')
    invalid_password_pattern = re.compile(r'Failed password')
    invalid_user_pattern = re.compile(r'Invalid user')
    break_in_attempt_pattern = re.compile(r'POSSIBLE BREAK-IN ATTEMPT!')

    bytes_read = len(entry.message)
    logger.debug(f'Received {bytes_read} bytes')

    if successful_login_pattern.search(entry.message):
        logger.info('Successfully logged in')
        return "Successful login"
    elif failed_login_pattern.search(entry.message):
        logger.warning("Failed password")
        return "Failed password"
    elif connection_closed_pattern.search(entry.message):
        logger.warning("Connection closed")
        return "Connection closed"
    elif invalid_password_pattern.search(entry.message):
        logger.error("Invalid password")
        return "Invalid password"
    elif invalid_user_pattern.search(entry.message):
        logger.error("Invalid user")
        return "Invalid user"
    elif break_in_attempt_pattern.search(entry.message):
        logger.critical("BREAK-IN ATTEMPT")
        return "BREAK-IN ATTEMPT"
    else:
        return "Another message"


def get_random_entries_for_random_user(logs, n):
    entries_with_users = dict()

    for entry in logs:
        user_entry = get_user_from_log(entry)
        if user_entry is not None:
            if user_entry not in entries_with_users:
                entries_with_users[user_entry] = [entry]
            else:
                entries_with_users[user_entry].append(entry)

    users = list(entries_with_users.keys())
    user = random.choice(users)
    selected_logs = random.sample(entries_with_users[user], n)
    return selected_logs


def most_common_and_rarest_entries(logs):
    entries_with_users = dict()

    for entry in logs:
        user_entry = get_user_from_log(entry)
        if user_entry is not None and get_message_type(entry) == "Successful login":
            if user_entry not in entries_with_users:
                entries_with_users.setdefault(user_entry, [entry])
            else:
                entries_with_users[user_entry].append(entry)

    rarest_user = min(entries_with_users, key=lambda user: len(entries_with_users[user]))
    most_common = max(entries_with_users, key=lambda user: len(entries_with_users[user]))

    return rarest_user, most_common


def print_logs(list):
    for entry in list:
        print(entry)


if __name__ == '__main__':
    logs = read_ssh_logs("SSH.log")
    print(most_common_and_rarest_entries(logs))
