
def sort_log(logs, element):
    try:
        sorted_logs = sorted(logs, key=lambda log: log[element])
        return sorted_logs
    except IndexError:
        print("Index out of range")
        return []


def get_entries_by_addr(logs, hostname):
    logs_ips = []
    for log in logs:
        if log[0] == hostname:
            logs_ips.append(log)
    return logs_ips


def get_entries_by_code(logs, code: int):
    logs_codes = []
    for log in logs:
        if log[3] == code:
            logs_codes.append(log)
    return logs_codes


def get_failed_reads(logs, return_as_one_list: bool):
    logs_5 = []
    logs_4 = []
    for log in logs:
        if 400 <= log[3] <= 599:
            if log[3] > 499:
                logs_5.append(log)
            else:
                logs_4.append(log)

    if return_as_one_list:
        return logs_4 + logs_5
    else:
        return logs_4, logs_5


def get_entries_by_extension(logs, extension):
    logs_extension = []
    for log in logs:
        if log[2].split()[1].endswith(extension):
            logs_extension.append(log)
    return logs_extension


def print_entries(logs):
    for log in logs:
        print(log)
