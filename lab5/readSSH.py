import re
import sys
import logging
from collections import namedtuple
from datetime import datetime
from statistics import mean, stdev
import random

log = namedtuple('log', ['date', 'name', 'process', 'num', 'message'])

logger = logging.getLogger(__name__)
logging.basicConfig(filename='readSSH.log', level=logging.INFO)


def read_ssh_logs(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield parse_line(line)


def parse_line(line):
    pattern = re.compile(
        r'(?P<date>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+'
        r'(?P<name>\S+)\s+'
        r'(?P<process>\S+)\[(?P<num>\d+)\]:\s+'
        r'(?P<message>.*)'
    )

    match = pattern.match(line)
    data = match.groups()

    # W tym momencie date jest typu TUPLE więc nie ma możliwości
    # odwołać się do danych za pomocą nazw zamiast indeksów

    #     File
    #     "C:\Study\Programming\Python\JezykiSkryptowe_Lab\lab5\readSSH.py", line 38, in parse_line
    #       date = datetime.strptime(data['date'], '%b %d %H:%M:%S')
    #                                ~~~~^^^^^^^^
    #
    #     TypeError: tuple indices must be integers or slices, not str

    date = datetime.strptime(data[0], '%b %d %H:%M:%S')
    name = data[1]
    process = data[2]
    num = int(data[3])
    message = data[4]

    return log(date, name, process, num, message)

    # try:
    #     if sys.argv[1] == "tuple":
    #         data = match.groups()
    #         date = datetime.strptime(data[0], '%b %d %H:%M:%S')
    #         name = data[1]
    #         process = data[2]
    #         num = int(data[3])
    #         message = data[4]
    #
    #         return log(date, name, process, num, message)
    #     elif sys.argv[1] == "dictionary":
    #         data = match.groupdict()
    #         log_dict = {
    #             "date": datetime.strptime(data.get("date"), '%b %d %H:%M:%S')
    #             "name": data.get("name"),
    #             "process": data.get("process"),
    #             "num": int(data.get("num")),
    #             "message": data.get("message")
    #         }
    #         return log_dict
    #     else:
    #         raise ValueError("Choose a valid 'tuple' or 'dictionary'")
    # except IndexError:
    #     raise ValueError("Arguments not provided")


def get_ipv4s_from_log(entry):
    ipv4_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    addresses = ipv4_pattern.findall(entry.message)
    return addresses


def get_user_from_log(entry):
    user_pattern = re.compile(r'\bAccepted password for (\S+)\b|'
                              r'\bFailed password for (?!invalid)(\S+)\b|'
                              r'\bsession closed for user (\S+)\b|'
                              r'\bsession opened for user (\S+)\b')
    match = user_pattern.match(entry.message)
    if match:
        for name in match.groups():
            if name is not None:
                return name
    else:
        return None


def get_message_type(entry):
    successful_login_pattern = re.compile(r'\bsession opened for user (\S+)\b')
    closed_login_pattern = re.compile(r'\bsession closed for user (\S+)\b')
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
    elif closed_login_pattern.search(entry.message):
        logger.info('Session closed')
        return "Session closed"
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
        entry_user = get_user_from_log(entry)
        if entry_user is not None:
            if entry_user not in entries_with_users:
                entries_with_users[entry_user] = [entry]
            else:
                entries_with_users[entry_user].append(entry)

    users = list(entries_with_users.keys())
    user = random.choice(users)
    selected_logs = random.sample(entries_with_users[user], n)
    return selected_logs


def calculate_durations(logs):
    durations = list()
    users = dict()

    start_time, end_time = datetime, datetime
    for entry in logs:

        if get_message_type(entry) == "Successful login":
            start_time = entry['date']

        elif get_message_type(entry) == "Session closed":
            end_time = entry['date']
            time = (end_time - start_time).total_seconds()

            durations.append(time)
            user = get_user_from_log(entry)
            if user not in users:
                users[user] = [time]
            else:
                users[user].append(time)

    global_mean = mean(durations)
    global_stdev = stdev(durations)

    user_stats = {}
    for user, user_durations in users.items():
        user_mean = mean(user_durations)
        user_stdev = stdev(user_durations)
        user_stats[user] = (user_mean, user_stdev)

    # W tym momencie user_stats ma tylko usera None, nie wiem czemu ten problem wystepuje
    # poniewaz get_message_type(entry) == "Session closed" znajduje w logu usera,
    # ale user = get_user_from_log(entry) nie znajduję, chociaż mają taki samy pattern dla wyszukiwania usera

    return global_mean, global_stdev, user_stats


def most_common_and_rarest_entries(logs):
    entries_with_users = dict()

    for entry in logs:
        user_entry = get_user_from_log(entry)
        if user_entry is not None and get_message_type(entry) == "Successful login":
            if user_entry not in entries_with_users:
                entries_with_users[user_entry] = 1
            else:
                entries_with_users[user_entry] += 1

    rarest_user = min(entries_with_users, key=lambda user: entries_with_users[user])
    most_common = max(entries_with_users, key=lambda user: entries_with_users[user])

    return rarest_user, most_common


def run_through_logs(list):
    for entry in list:
        print(get_user_from_log(entry))


if __name__ == '__main__':
    print(run_through_logs(read_ssh_logs("SSH.log")))
