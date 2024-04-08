import os
import sys
import shutil
import json
from datetime import datetime


def create_backup_zip(source_dir, backup_dir):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    dirname = os.path.basename(os.path.normpath(source_dir))
    backup_file_name = f"{timestamp}-{dirname}"
    backup_path = os.path.join(backup_dir, backup_file_name)

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    shutil.make_archive(backup_path, 'zip', source_dir)
    return backup_file_name


def update_backup_history(backup_dir, backup_record):
    backup_history_file = 'backup_history.json'
    history_path = os.path.join(backup_dir, backup_history_file)
    if os.path.exists(history_path):
        with open(history_path, 'r+') as file:
            history = json.load(file)
            history.insert(0, backup_record)
            file.seek(0)
            json.dump(history, file, indent=5)
    else:
        with open(history_path, 'w') as file:
            json.dump([backup_record], file, indent=5)





if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     sys.exit(1)
    #
    # source_dir = sys.argv[1]
    source_dir = "C:\\Study\\Programming\\Python\\JezykiSkryptowe_Lab\\lab4\\for backups"
    backup_dir = os.getenv('BACKUPS_DIR', os.path.join(os.path.expanduser('~'), '.backups'))

    backup_record = {
        'name': create_backup_zip(source_dir, backup_dir),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'location': os.path.abspath(source_dir),
        'folder': os.path.basename(backup_dir)
    }

    update_backup_history(backup_dir, backup_record)

    print("Backup Created")
