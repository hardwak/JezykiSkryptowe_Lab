import re
from datetime import datetime
from ipaddress import IPv4Address

from lab6.SSHLogEntry import SSHLogEntry_FailedPassword, SSHLogEntry_AcceptedPassword, SSHLogEntry_Error, SSHLogEntry_Other

# from SSHUser import SSHUser


class SSHLogJournal:
    def __init__(self):
        self.journal = []

    def __len__(self):
        return len(self.journal)

    def __iter__(self):
        return iter(self.journal)

    def __contains__(self, item):
        return item in self.journal

    def append(self, log):
        pattern = re.compile(
            r'(?P<date>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+'
            r'(?P<name>\S+)\s+'
            r'(?P<process>\S+)\[(?P<num>\d+)\]:\s+'
            r'(?P<message>.*)'
        )
        failed_password_pattern = re.compile(r'\bFailed password\b')
        accepted_password_pattern = re.compile(r'\bAccepted password\b')
        error_pattern = re.compile(r'\berror\b')

        match = pattern.match(log)
        data = match.groups()

        date = datetime.strptime(data[0], '%b %d %H:%M:%S')
        name = data[2]
        pid = int(data[3])

        if failed_password_pattern.search(log):
            log_entry = SSHLogEntry_FailedPassword(date, name, pid, log)
        elif accepted_password_pattern.search(log):
            log_entry = SSHLogEntry_AcceptedPassword(date, name, pid, log)
        elif error_pattern.search(log):
            log_entry = SSHLogEntry_Error(date, name, pid, log)
        else:
            log_entry = SSHLogEntry_Other(date, name, pid, log)

        self.journal.append(log_entry)

        return log_entry

    def get(self, index):
        return self.journal[index]

    def find_by_ip(self, ip_address):
        logs = []

        for log in self.journal:
            if log.get_ip_v4_address() == IPv4Address(ip_address):
                logs.append(log)

        return logs


# if __name__ == '__main__':
#     lines = [
#         "Dec 10 07:07:45 LabSZ sshd[24206]: Failed password for invalid user test9 from 52.80.34.196 port 36060 ssh2",
#         "Dec 10 07:08:28 LabSZ sshd[24208]: pam_unix(sshd:auth): check pass; user unknown",
#         "Dec 10 07:28:00 LabSZ sshd[24241]: Failed password for root from 112.95.230.3 port 50999 ssh2",
#         "Dec 10 07:51:15 LabSZ sshd[24324]: Failed password for invalid user support from 195.154.37.122 port 56539 ssh2",
#         "Dec 10 07:51:15 LabSZ sshd[24324]: error: Received disconnect from 195.154.37.122: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]",
#         "Dec 10 07:51:17 LabSZ sshd[24326]: reverse mapping checking getaddrinfo for 195-154-37-122.rev.poneytelecom.eu [195.154.37.122] failed - POSSIBLE BREAK-IN ATTEMPT!",
#         "Dec 10 07:51:18 LabSZ sshd[24326]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=195.154.37.122  user=uucp",
#         "Dec 10 07:51:20 LabSZ sshd[24326]: Failed password for uucp from 195.154.37.122 port 59266 ssh2",
#         "Dec 10 07:51:20 LabSZ sshd[24326]: error: Received disconnect from 195.154.37.122: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]",
#         "Dec 10 07:53:26 LabSZ sshd[24329]: Connection closed by 194.190.163.22 [preauth]",
#         "Dec 10 09:31:34 LabSZ sshd[24678]: Connection closed by 104.192.3.34 [preauth]",
#         "Dec 10 09:32:20 LabSZ sshd[24680]: Accepted password for fztu from 119.137.62.142 port 49116 ssh2",
#         "Dec 10 11:40:46 LabSZ sshd[27962]: Accepted password for fztu from 113.118.187.34 port 31938 ssh2",
#         "Dec 10 13:46:40 LabSZ sshd[4772]: Accepted password for fztu from 113.118.187.34 port 30950 ssh2"
#     ]
#
#     journal = SSHLogJournal()
#     for line in lines:
#         journal.append(line)
#
#     users_and_logs = [
#         SSHUser("user1", "Dec 10 07:51:18"),
#         SSHUser("user2", "Dec 12 02:12:32"),
#         SSHUser("#@$%", "Dec 13 12:23:57")
#     ]
#
#     for i in range(3):
#         users_and_logs.append(journal.journal[i])
#
#     for item in users_and_logs:
#         print(item.validate())
