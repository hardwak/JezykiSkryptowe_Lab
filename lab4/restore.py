import shutil
import sys
import os
import json


def restore(backup_dir):
    backup_history_file = 'backup_history.json'
    history_path = os.path.join(backup_dir, backup_history_file)
    if os.path.exists(history_path):
        with open(history_path, 'r+') as file:

            history = json.load(file)
            history_size = 0

            for entry in history:
                history_size += 1
                print(history_size, " - ", entry)

            choice = int(input("Pick num of record\n"))
            if choice < 1 or choice > history_size:
                raise ValueError("Not a valid choice")

            backup_to_restore = history[choice]
            backup_file = os.path.join(backup_dir, backup_to_restore['name'])

            target_dir = backup_to_restore['location']
            shutil.unpack_archive(backup_file + '.zip', target_dir, 'zip')


if __name__ == "__main__":
    backup_dir = os.getenv('BACKUPS_DIR', os.path.join(os.path.expanduser('~'), '.backups'))
    # 'C:\\Users\\ymher\\.backups'

    if len(sys.argv) == 2:
        backup_dir = sys.argv[1]

    restore(backup_dir)
