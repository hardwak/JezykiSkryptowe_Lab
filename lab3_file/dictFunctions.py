def entry_to_dict(log):
    keys = ["ip", "timestamp", "request", "status_code", "num_of_bytes"]
    dictionary = {keys[i]: log[i] for i in range(len(log))}
    return dictionary


def log_to_dict(logs):
    dictionary = {}
    for log in logs:
        dict_entry = entry_to_dict(log)
        if log[0] in dictionary:
            dictionary[log[0]].append(dict_entry)
        else:
            dictionary[log[0]] = [dict_entry]
    return dictionary


def get_addresses(logs_dict):
    return list(logs_dict.keys())


def print_dict_entry_dates(logs_dict):
    for addr, entries in logs_dict.items():
        num_of_code200 = 0
        for entry in entries:
            if entry["status_code"] == 200:
                num_of_code200 += 1

        print("---------------------------------------------------------------------")
        print(f"Address: {addr}")
        print(f"Number of entries: {len(entries)}")
        print(f"First entry: {entries[0]}")
        print(f"Last entry: {entries[-1]}")
        print(f"{num_of_code200} of {len(entries)} entries had code 200")
        print("---------------------------------------------------------------------")
