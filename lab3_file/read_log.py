import sys
import datetime
import logFunctions


def read_log():
    logs = []
    # line = ("rs6000.cmp.ilstu.edu - - [21/Jul/1995:00:43:42 -0400] \"GET "
    #         "/shuttle/technology/sts-newsref/stsref-toc.html HTTP/1.0\" 200 84905")
    for line in sys.stdin:

        parts = line.split()
        host = parts[0]
        timestamp = datetime.datetime.strptime(parts[3][1:], '%d/%b/%Y:%H:%M:%S')

        request = parts[5]
        if not parts[5].endswith('\"'):
            request += " " + parts[6]
        if not parts[6].endswith('\"'):
            request += " " + parts[7]

        try:
            status_code = int(parts[-2])
        except ValueError:
            status_code = parts[-2]

        try:
            bytes_sent = int(parts[-1])
        except ValueError:
            bytes_sent = parts[-1]

        logs.append((host, timestamp, request, status_code, bytes_sent))
    return logs


if __name__ == "__main__":
    logs = read_log()
    logFunctions.print_entries(logFunctions.get_entries_by_extension(logs, ".gif"))
